'''
This module retrieves filtered data from the cov19API
as a json file and returns specific requested parts
of the json file which are either used in calculations
or returned as is. The filtered location can be changed
in the config file. The module also has functionality to
schedule the data to be updated and returned at a specific
time.

'''
import sched
import time
import logging
from uk_covid19 import Cov19API
from config import get_config_data
from logger import log , setup_logging

covid_update_scheduler = sched.scheduler(time.time,time.sleep)

local_data = []
national_data = []

Covid_logger = logging.getLogger(__name__)
setup_logging(Covid_logger)

def parse_csv_data(csv_filename:str)->None:
    '''
    Function
    --------
        opens a file and returns the lines of the file
    Parameters
    ----------
    csv_filename : str
        name of the file to be opened
    Returnsp
    --------
    lines : list
        list containing lines of the opened file
    '''
    log(Covid_logger, 'Readlines from csv file')
    with open(csv_filename) as file:
        lines = file.readlines()
    file.close()
    return lines

def process_covid_csv_data(covid_csv_data:list) ->int:
    '''
    Function
    --------
        takes a list of data (in csv format) and retrieves
        specific values from the data
    Parameters
    ----------
    covid_csv_data : list
        list containg data to be processed by the function
    Returns
    --------
    last7days_cases : int
        covid cases in the last 7 days from csv file
    current_hospital_cases : int
        current hospital cases from csv file
    total_deaths : int
        current cumulative deaths from csv file
    '''
    array_of_data = []
    last7days_cases = 0
    current_hospital_cases = 0
    total_deaths = 0
    for line in covid_csv_data:
        data = line.split(',')
        array_of_data.append(data)
    for i in range(7):
        try:
            if isinstance(array_of_data[i + 3][6], str):
                number = array_of_data[i + 3][6]
                last7days_cases += int(number)
        except Exception as excep:
            log(Covid_logger, excep)
            
    while_counter = 1
    while total_deaths == 0:
        if not array_of_data[while_counter][4] == "":
            total_deaths = int(array_of_data[while_counter][4])
        else:
            while_counter += 1
    current_hospital_cases = int(array_of_data[1][5])
    log(Covid_logger, 'process_covid_csv_data returned data')
    return last7days_cases , current_hospital_cases , total_deaths

def covid_API_request(location:str = get_config_data('local_location') ,
                      location_type:str = get_config_data('local_location_type')) -> dict:
    '''
    Function
    --------
        takes in two arguments and updates global list
        structures with location data in the form of a dictionary
    Parameters
    ----------
    location : string
        location is used to form a query which is passed
        into the covid19 API
    location_type : string
        location_type is used to form a query which is passed
        into the covid19 API.
    Returns
    --------
    api.get_json()['data']:
        dictionary containing data covid data
    '''
    Exeter_only = ['areaType=' + location_type,'areaName='+ location]
    cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate",
    "cumDailyNsoDeathsByDeathDate":"cumDailyNsoDeathsByDeathDate",
    "hospitalCases":"hospitalCases"
    }

    api = Cov19API(filters= Exeter_only, structure=cases_and_deaths)
    if location == 'Exeter':
        local_data.clear()
        local_data.append(api.get_json()['data'])
        log(Covid_logger, 'Local covid data updated')
    elif location == 'England':
        national_data.clear()
        national_data.append(api.get_json()['data'])
        log(Covid_logger, 'National covid data updated') 
    return api.get_json()

def process_api_data(list_of_dictionary:dict)->int:
    '''
    Function
    --------
        Takes data in a json format and returns three values processed
        from the data
    Parameters
    ----------
    Returns
    -------
     total_deaths : int
        The cumulative number of deaths
    current_hospital_cases : int
        The current number of hospital cases result of covid
    last7days_cases : int
        The total number of cases over the last 7 days
    '''
    total_deaths = 0
    current_hospital_cases = 0
    last7days_cases = 0

    list_of_dictionary = list_of_dictionary['data']

    for value in enumerate(list_of_dictionary):

        if isinstance(value[1]['cumDailyNsoDeathsByDeathDate'], int):
            if(int(value[1].get('cumDailyNsoDeathsByDeathDate'))) > 0:
                total_deaths = value[1].get('cumDailyNsoDeathsByDeathDate')
                break
    for value in enumerate(list_of_dictionary):
        if isinstance(value[1]['hospitalCases'], int):
            current_hospital_cases = value[1].get('hospitalCases')
    last7days_count = 0
    for value in enumerate(list_of_dictionary):
        if last7days_count < 7:
            if isinstance(value[1]['newCasesBySpecimenDate'], int):
                last7days_cases += value[1].get('newCasesBySpecimenDate')
                last7days_count +=1
    log(Covid_logger, 'New total_deaths , current_hospital_cases and ' +
     'last7days_cases calculated')
    return total_deaths , current_hospital_cases, last7days_cases

def return_api_data(local_or_national:str) -> list:
    '''
    Function
    --------
        Checks whether the data is local or national and
        returns an according list
    Parameters
    ----------
    local_or_national : str
        Used to determine which return value is chosen
    Returns
    -------
    national_data : list
        list containing national data
    local_data : list
        list containing local data
    '''
    if local_or_national == 'local':
        log(Covid_logger, 'Returning local data')
        return {'data' :local_data[0]}
    elif local_or_national == 'national':
        log(Covid_logger, 'Returning national data')
        return {'data':national_data[0]}
    else:
        return None

def schedule_covid_updates(update_name:str,update_interval:int = get_config_data('covid_default_wait')) ->dict:
    '''
    Function
    --------
        Schedules a function to be executed after a given delay
    Parameters
    ----------
    udpate_interval : int
        Time in seconds for which to delay calling news_API_request
    update_name : str
        Identifier for the update
    Returns
    -------
        Dictionary containing the update_name as the key and the scheduler object as a value
    '''
    log(Covid_logger, 'Scheduling ' + update_name + ' a news update in '
        + str(update_interval) + 'seconds' )
    return {update_name : [covid_update_scheduler.enter(update_interval , 1 , covid_API_request,
                        [get_config_data('national_location'),
                         get_config_data('national_location_type')]),
                        covid_update_scheduler.enter(update_interval , 1 , covid_API_request)]}


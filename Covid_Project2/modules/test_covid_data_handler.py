'''
Module is used for testing covid_data_handler
'''
from app import remove_from_scheduler
from covid_data_handler import (parse_csv_data, process_api_data, return_api_data,
covid_update_scheduler, process_covid_csv_data, covid_API_request, schedule_covid_updates)

def test_parse_csv_data() -> None:
    '''
    Function
    --------
    Tests the length of the csv is equal to 639
    '''
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data()-> None:
    '''
    Function
    --------
    Tests that the values returned from process_csv_data are correct
    '''
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data (parse_csv_data('nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request()->None:
    '''
    Function
    --------
    Tests the data returned from covid_API_request is in the format of a dictionary
    '''
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates()-> None:
    '''
    Function
    --------
    Tests a covid update can be scheduled 
    '''
    sched_update = schedule_covid_updates('update test')['update test']
    covid_update_scheduler.cancel(sched_update[0])
    covid_update_scheduler.cancel(sched_update[1])

def test_return_api_data()->None:
    '''
    Function
    --------
    Tests that return_api_data returns data in the format of a dictionary
    '''
    covid_API_request()
    covid_API_request('England','nation')
    assert isinstance(return_api_data('local'),dict)
    assert isinstance(return_api_data('national'),dict)

def test_process_api_data()->None:
    '''
    Function
    --------
    Tests that the variables returned from process_api_data with argument
    covid_API_request('England','nation') are all integers 
    '''
    a , b , c = process_api_data(covid_API_request('England','nation'))
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert isinstance(c, int)

    


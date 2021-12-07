'''
Module reads the config file and returns requested data
'''
import json

def get_config_data(config_request:str):
    '''
    Function
    --------
        Opens up json configuration file and returns requested
        data from the file
    Parameters
    ----------
        config_request : str
    A string value containing term used to identify return value
    Returns
    -------
    data : str / int
        value mapped to config_request returned from the json file
    '''
    with open('config.JSON') as config_file:
        data = json.load(config_file)
        try:
            data = data[config_request]
            return data
        except:
            print('Error occured in config file, unable to log')

'''
Module is used for logging information that occurs during runtime.
'''
import logging
from config import get_config_data

def setup_logging(logger:object) -> None:
    '''
    Function
    --------
        Sets the file and format aswell as the logger level of the logger
        object passed into it.
    parameters
    ----------
    A logger object
    '''
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
    if get_config_data('logging_level') == "INFO":
        file_handler = logging.FileHandler('info.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    elif get_config_data('logging_level') == "Error":
        file_handler = logging.FileHandler('Error.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.ERROR)
def log(logger:object, message:str) -> None:
    '''
    Function
    --------
        Logs the info depending on the logging level
    parameters
    ----------
        message : str
    information to be appended to the log
    '''
    if get_config_data('logging_level') == "INFO":
        logger.info(message)
    elif get_config_data('logging_level') == "ERROR":
        logger.error(message)

'''
This module retrieves news articles from
a news api and performs functions such as removing
articles from a list, returning the list and scheduling,
the list to be updated.
'''
import sched
import time
import logging
import requests
from config import get_config_data
from logger import log , setup_logging

news_update_scheduler = sched.scheduler(time.time,time.sleep)

removed_article_titles = []
ARTICLE_LIST = []

News_logger = logging.getLogger(__name__)
setup_logging(News_logger)

def news_API_request(covid_terms:str = get_config_data('covid_terms'))-> list: 
    '''
    Function
    ----------
        Makes a request using the request module to newsapi.org
        where it retrieves a list of articles containing the covid_terms
    Parameters
    ----------
        covid_terms : str
    A string value containing terms that are passed
    into the request query to filter the returned articles
    Returns
    --------
        ARTICLE_LIST : list
    list containing dictionarys of news articles
    '''
    covid_terms = covid_terms.replace(' ','&')
    try:
        response = requests.get('https://newsapi.org/v2/top-headlines?q='+covid_terms+'&language='
                            +get_config_data("news_language")+'&apiKey='+get_config_data('api_key'))
        
        ARTICLE_LIST.append(response.json()['articles'])
    except requests.ConnectionError as exc:
        log(News_logger, 'Connecton Error for newsapi')
        log(News_logger, exc)
    log(News_logger, 'News articles updated from API')
    return ARTICLE_LIST

def update_news(update_name:str, update_interval:int = get_config_data('news_default_wait'))->dict:
    '''
    Function
    ----------
        Schedules the articles_list to be updated by
        calling news_API_request at a desired time.
    Parameters
    ----------
        update_interval : int
    Time in seconds for which to delay calling news_API_request
        update_name : str
    Identifier for the update
    Returns
    --------
        Dictionary containing the update_name as the key and the scheduler object as a value
    '''
    try:
        log(News_logger, 'Scheduling ' + update_name + ' a covid update in '
        + str(update_interval) + 'seconds\n')
        return { update_name : news_update_scheduler.enter(update_interval, 1 , news_API_request)}
    except TypeError as exc:
        log(News_logger, exc)
        log(News_logger, 'TypeError occured')
        return { update_name : news_update_scheduler.enter(update_interval, 1 , news_API_request)}

def article_compare(article_list_param:list)->list:
    '''
    Function
    ----------
        checks whether an article title is in the removed article_title_list and
        does not append that article to the article list if the case is true
    Parameters
    ----------
        article_list : list
    A list containing dictionarys of articles
    Returns
    --------
        A list containing dictionarys of articles
    '''
    try:
        list_of_articles = []
        for article in article_list_param[0]:
            if article['title'] not in removed_article_titles:
                list_of_articles.append(article)
    except AttributeError as exc:
        log(News_logger, exc)
        log(News_logger, AttributeError)
    log(News_logger, 'Removed articles and returned news articles')
    return list_of_articles

def removed_article(article_title:str)->None:
    '''
    Function
    ----------
        Adds am article title to the removed_article_titles list
    Parameters
    ----------
        article_title : string
    Title of the article
    '''
    try:
        removed_article_titles.append(article_title)
        log(News_logger, 'Added a new title to removed_article_titles' )
    except AttributeError as exc:
        log(News_logger, exc)

def return_article_list()->list:
    '''
    Function
    ----------
        returns the article_list global variabe
    Returns
    --------
        article_list : list
    '''
    log(News_logger , 'return ARTICLE_LIST')
    return ARTICLE_LIST



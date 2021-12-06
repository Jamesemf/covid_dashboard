'''
Module is used for testing covid_news_handler
'''
from covid_news_handling import (news_API_request, return_article_list,
 update_news , article_compare, removed_article_titles, removed_article, news_update_scheduler)

def test_news_API_request()->None:
    '''
    Function
    -------
    Tests that news_API_requests has a default argument that returns the same data with or
    without the filter string being passed into it 
    '''
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news() -> None:
    '''
    Function
    -------
    Tests that a news update can be scheduled with a label only
    '''
    sched_update = update_news('test')['test']
    news_update_scheduler.cancel(sched_update)

def test_article_compare()->None:
    '''
    Function
    -------
    Tests that an article with a removed title is not appended to a list if it is already in the removed_article_titles list
    '''
    removed_article_titles.append('Article title 1')
    article_list = [[{'title': 'Article title 1'}, {'title':'Article title 2'} , {'title':'Article title 3'}]]
    assert article_compare(article_list)[0]['title'] == 'Article title 2'
    removed_article_titles.remove('Article title 1')

def test_removed_article() ->None:
    '''
    Function
    -------
    Tests that an article title can be added to the removed_article_title list
    '''
    removed_article('I am a test')
    assert 'I am a test' in removed_article_titles
    removed_article_titles.remove('I am a test')

def test_return_article_list()->None:
    '''
    Funtion
    -------
    Tests that return_article_list() returns the intended list data type
    '''
    news_API_request()
    assert isinstance(return_article_list(), list)







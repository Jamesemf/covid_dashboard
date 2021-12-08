'''
Module is used for testing app.py
'''
from app import (news_handling, remove_from_scheduler, remove_update, schedule_handling, time_difference, list_scheduled_updates)
from covid_news_handling import removed_article_titles
from covid_data_handler import covid_update_scheduler

def test_news_handling():
    '''
    Function
    --------
    Tests that a news article title can be added to the list
    '''
    news_handling('news_title')
    removed_article_titles.remove('news_title')

def test_schedule_handling():
    '''
    Function
    --------
    Tests that updates with variation in the data required to update
    and whether they're repeatable are able to scheduled
    '''
    schedule_handling(True, 'a_label', '12:00', False, True, False )
    schedule_handling(True, 'b_label', '12:00', False, False, True )
    schedule_handling(True, 'c_label', '12:00', False, True, True )
    schedule_handling(True, 'd_label', '12:00', True, True, True )
    

def test_time_difference():
    '''
    Function
    --------
    Tests that the time difference can be calculated and returned as a float
    '''
    assert isinstance(time_difference('12:00'), float)

def test_remove_update():
    '''
    Function
    --------
    Tests that an update can be remove from the update list
    '''
    list_scheduled_updates.clear()
    schedule_handling(True, 'remove_label', '12:00', False, False, True )
    assert(len(list_scheduled_updates) == 1) 
    remove_update('remove_label')
    assert(len(list_scheduled_updates) == 0) 
    
def test_identical_update_label_not_added():
    '''
    Function
    --------
    Tests that two identical labeled updates cannot be added 
    '''
    list_scheduled_updates.clear()
    schedule_handling(True, 'a_label', '12:00', False, True, False )
    schedule_handling(True, 'a_label', '12:00', False, True, False )
    assert(len(list_scheduled_updates) == 1) 
    list_scheduled_updates.clear()
    






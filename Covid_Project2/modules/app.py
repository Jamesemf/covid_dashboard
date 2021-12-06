'''
This module creates a html webpage using flask and dispalys, covid data
and news articles retrieved from covid_data_handler and covid_news_handler.
The module also allows you to schedule updates to occur to the data and news
aswell as removing these scheduled updates and news articles.
'''
import logging
import unittest
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect
from covid_data_handler import (covid_API_request , process_api_data, return_api_data
                                ,schedule_covid_updates , covid_update_scheduler)
from covid_news_handling import (return_article_list , removed_article,article_compare
                                ,update_news , news_API_request ,  news_update_scheduler)
from config import get_config_data
from logger import log , setup_logging
import pytest

app = Flask(__name__)

list_scheduled_updates = []
covid_updates = []
news_updates = []

covid_API_request()
covid_API_request(get_config_data('national_location'),
                  get_config_data('national_location_type'))
news_API_request()

logger = logging.getLogger(__name__)
setup_logging(logger)
if get_config_data('logging_level') == 'INFO':
    logging.basicConfig(filename ='websitelog.log', level=logging.INFO)
elif get_config_data('logging_level') == 'ERROR':
    logging.basicConfig(filename ='websitelog.log', level=logging.ERROR)
else:
    log(logger, 'Unable to setup logging correctly. Unsuitable return from config file')



def restore_updates_from_log()-> None:
    '''
    Function
    --------
    Restores the scheduled updates from the log
    '''
    with open('websitelog.log') as logfile:
        for line in logfile.readlines():
            if line[5:13] == 'werkzeug' and line[68:75] == 'update=':
                line_dictionary = {'update_title':'' , 'update_time' :'' ,
                                   'covid_data': False, 'news_data' : False , 'repeat' : False}
                args = line.split('&')
                line_dictionary['update_time'] = str(args[0][75:77])+ ':'+str(args[0][80::])
                line_dictionary['update_title'] = args[1].split('=')[1]
                if len(args) == 5:
                    line_dictionary['covid_data'] = True
                    line_dictionary['news_data'] = True
                    line_dictionary['repeat'] = True
                elif len(args) == 4:
                    if 'covid-data' in args[2] or 'covid-data' in args[3]:
                        line_dictionary['covid_data'] = True
                    elif 'news' in args[2] or 'news' in args[3]:
                        line_dictionary['news_data'] = True
                    elif 'repeat' in args[2]:
                        line_dictionary['repeat'] = True
                elif len(args) == 3:
                    if 'covid-data' in args[2]:
                        line_dictionary['covid_data'] = True
                    elif 'news' in args[2]:
                        line_dictionary['news_data'] = True
                schedule_handling(True,
                line_dictionary['update_title'],
                line_dictionary['update_time'],
                line_dictionary['repeat'],
                line_dictionary['covid_data'],
                line_dictionary['news_data'])
            elif line[5:13] == 'werkzeug' and line[68:80] == 'update_item=':
                args = line.split('=')[1]
                title = args.split(' ')[0]
                try:
                    remove_update(title)
                except Exception as error:
                    log(logger, 'Unable to remove an update in restore update on startup')
                    log(logger, error)
            elif '__main__' in line and '**' in line:
                try:
                    remove_update(line.split('**')[1].strip())
                except Exception as error:
                    log(logger, 'Unable to remove an update that had occured in startup')
                    log(logger, error)
                    break

@app.route('/index')
def handling():
    '''
    Function
    --------
        function for managing news_handling and schedule_handling.
        schedule_handling is always call whereas news handling
        is called if an article has been removed.
        function then redirects to app.home().
    Returns
    --------
        A redirect to the main body of app
    '''
    if request.args.get('notif'):
        news_handling(request.args.get('notif'))
    schedule_handling()
    return redirect('/')

def news_handling(notif:str)->None:
    '''
    Function
    ----------
        Calls the removed_article method and passes it notif.
    Parameters
    --------
        notif : str
    The title of the article
    '''
    try:
        removed_article(notif)
        log(logger, 'Removed an article')
    except TypeError as error:
        log(logger, 'Fail to remove news article ' + str(notif))
        log(logger, error)

def schedule_handling(restore_update:bool = False , label:str = None , time:str = None,
                      repeat:bool = False , covid_checked:bool = False,
                       news_checked:bool = False) ->None:
    '''
    Function
    ----------
        Retrieves data input into the webpage and checks whether an update of the
        same name exists before creating either a scheduled news update, scheduled
        covid update or both. A scheduled update dictionary is created and
        this update is then appened to the list_scheduled_updates.
        The shedulers are then run.
    Parameters
    --------
        restoreUpdate : boolean
    whether the schedules are being restored from the log file
        label : str
    The title of the update
        time : str
    The time the update should occur at
        repeat : boolean
    Whether the update should repeat
        covid_checked : boolean
    Whether covid dataa should be updated
        news_checked : boolean
    whether news should be updated
    '''
    if restore_update is False:
        if request.args.get('update_item'):
            remove_update(request.args.get('update_item'))
        label = request.args.get('two')
        time = request.args.get('update')
        if request.args.get('repeat'):
            repeat = True
        if request.args.get('covid-data'):
            covid_checked = True
        if request.args.get('news'):
            news_checked = True
    if label is not None and time is not None and (covid_checked or news_checked):
        title_list = [i['title'] for i in list_scheduled_updates]
        if label not in title_list:
            if covid_checked:
                covid_data_update = schedule_covid_updates(label, time_difference(time))
                covid_updates.append(covid_data_update)
            if news_checked:
                news_update = update_news(label, time_difference(time))
                news_updates.append(news_update)

            content = ['Time | ' + str(time),'Covid_update | ' + str(covid_checked),
                       'News_update | ' +str(news_checked),'Repeat | '+ str(repeat)]
            scheduled_updates = {'title' : label , 'content' : content, 'time': time,
                                 'covid_update' : covid_checked , 'news_update' : news_checked,
                                 'repeat' : repeat}
            log(logger, 'New scheduled event :\n ' + label + str(content))
            list_scheduled_updates.append(scheduled_updates)
    log(logger, 'Size of list_scheduled_updates = ' + str(len(list_scheduled_updates)))
    news_update_scheduler.run(blocking = False)
    covid_update_scheduler.run(blocking = False)
@app.route('/')
def home() ->object:
    '''
    Function
    ----------
        Function retrieves local and national covid data from covid_data_handler module
        and news articles from covid_news_handling module and then displays them on a
        webpage
    Returns
    --------
        the render template for the format of the webpage along with all the
        data retrieved from the other modules to fill the webpage
    '''
    local_data = process_api_data(return_api_data('local'))
    national_data = process_api_data(return_api_data('national'))
    list_of_news_articles = article_compare(return_article_list())
    updates_to_display = list_scheduled_updates
    if len(updates_to_display) == 0:
        updates_to_display = [{'title' : 'Currently there are no updates to display',
                               'content' : '', 'url' : '' }]
    news_to_display = list_of_news_articles[0:5]
    if len(news_to_display) == 0:
        news_to_display = [{'title' : 'Currently there are no articles to display',
                            'content' : '', 'url' : '' }]
    remove_from_scheduler(None)
    return render_template('index.html',
                           image = get_config_data('image_file'),
                           title = get_config_data('webpage_title'),
                           location = get_config_data('local_location'),
                           nation_location = get_config_data('national_location'),
                           local_7day_infections = local_data[2],
                           hospital_cases = national_data[1],
                           deaths_total = national_data[0],
                           national_7day_infections = national_data[2],
                           news_articles = news_to_display,
                           updates = updates_to_display)

def remove_from_scheduler(update_title:str) -> None:
    '''
    Function
    ----------
        Function removes a update from the scheduler if the update has been
        cancelled or removes the update from the webpage if the update has
        already occured.
   parameters
   ----------
   update_title : string
       title of the update
    '''
    if update_title is not None:
        for updates in covid_updates:
            if update_title in updates:
                data = updates.get(update_title)
                covid_update_scheduler.cancel(data[0])
                covid_update_scheduler.cancel(data[1])
                covid_updates.remove(updates)
                log(logger, update_title + ' removed from covid scheduler')
        for updates in news_updates:
            if update_title in updates:
                data = updates.get(update_title)
                news_update_scheduler.cancel(data)
                news_updates.remove(updates)
                log(logger, update_title + ' removed from news scheduler')
    else:
        for update in list_scheduled_updates:
            for cov_up in covid_updates:
                if update['title'] in cov_up:
                    if cov_up[update['title']][0] not in covid_update_scheduler.queue:
                        if update['repeat']:
                            covid_updates.remove(cov_up)
                            covid_data_update = schedule_covid_updates(update['title'],
                            time_difference(update['time']))
                            covid_updates.append(covid_data_update)
                            log(logger, 'Rescheduling covid : ' + update['title'])
                        else:
                            list_scheduled_updates.remove(update)

                            log(logger, 'Removed ' + update['title'] +
                                ' from list_scheduled_updates')
                            log(logger, '**'+update['title'])
            for news_up in news_updates:
                if update['title'] in news_up:
                    if news_up[update['title']] not in  news_update_scheduler.queue:
                        if update['repeat']:
                            news_updates.remove(news_up)
                            news_update = update_news(update['title'],
                            time_difference(update['time']))
                            news_updates.append(news_update)
                            log(logger, 'Rescheduling news : ' + update['title'])
                        else:
                            try:
                                list_scheduled_updates.remove(update)
                                log(logger, 'Removed ' + update['title'] +
                                    ' from list_scheduled_updates')
                                log(logger, '**'+update['title'])
                            except Exception as error:
                                log(logger, error)
                                break

def time_difference(update_time:str) -> float:
    '''
    Function
    ----------
        Function calculates the number of seconds between the current time
        and the time update_time parameter passed into it
    parameters
    ----------
        update_time : str
    The time that the update should occur at
    Returns
    --------
        The number of seconds between the current time and update_time
    '''
    fmt = '%H:%M:%S'
    update_time = update_time+ ":00"
    now = datetime.now()
    now = now.strftime('%H:%M:%S')
    difference_time = datetime.strptime(update_time, fmt) - datetime.strptime(now, fmt)
    if difference_time.days < 0:
        difference_time = timedelta(
        days=0,
        seconds=difference_time.seconds,
        microseconds=difference_time.microseconds
    )
    log(logger, 'Calculated delay time')
    return difference_time.total_seconds()

def remove_update(title:str)->None:
    '''
    Function
    --------
    Remove an update from the scheduler and from the list_scheduled_updates
    that is displayed on the webpage
    parameters
    ----------
        title : str
    The title of the update to be removed
    '''
    for update in list_scheduled_updates:
        if update['title'] == title:
            try:
                
                remove_from_scheduler(update['title'])
                list_scheduled_updates.remove(update)
                log(logger , update['title'] + ' removed from list_scheduled_updates')
            except TypeError as error:
                log(logger , error)


log(logger,  '\n NEW EXECUTION \n')

if __name__ == '__main__':
    pytest.main()
    restore_updates_from_log()
    app.run()

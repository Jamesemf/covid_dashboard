# Introduction 

 The purpose of the covid dashboard project was to provide real time data on the current status of a country; in terms of its news, recent deaths, hospital cases and cumulative deaths in releation to covid-19. The project displays both quantative data in the central panel and relevant informative news articles on the right side of the interface. The project allows you to schedule updates to occur at a selected time to the central quantative data and news articles so that the interface is always displaying upto date information to the user.

## **Prerequisites** 
###### **Development version: 3.9.9**
Dependinces that are not in the installation are:

 - Libraies  
    - logging 
    - datetime 
    - time 
    - sched 
    - requests 
 - Internal modules 
    - config 
    - logger 
    - covid_data_handler
    - covid_news_handling
    - app 
 - Files 
    - config.json
    - nation_2021-10-28.csv
## **Installation**
Module dependencies for the covid dashboard are: 
 - flask
 - uk_covid19
 - pytest

## **Getting started**

##### **Configuration file**
A Json file used for configuration of the dashboard. Within the file options for configuration include.
 - 'image_file'
   - The name of the file containing the image to be displayed on the covid dashboard should be entered here. The .png should then be saved in the static folder of the application.
- 'webpage_title'
   - The displayed title of the dashboard can be entered here.
- 'api_key'
   - The api key required to retrieve news data is saved here 
- 'news_language'
   - The filtered language for news articles is set here. To find the other potential language options for filtering go to https://newsapi.org/docs/endpoints/sources
- 'covid_terms'
   - The terms used to filter the news articles. These can be changed if you wish for the interface to display articles relating to different subjects
- 'csv_filename'
   - The csv_file that contains past covid information
- 'news_default_wait'
   - the default wait time that news articles are sceduled for if no update time is entered. 
- 'national_location'
   - The national location where the quantative covid data is acquired from. 
- 'national_location_type'
   - The type of location it is. This can be identified by going to https://coronavirus.data.gov.uk/details/developers-guide/generic-api
- 'local_location'
   - The local location where the quantative covid data is acquired from 
- 'local_location_type'
   -The type of location it is. This can be identified by going to https://coronavirus.data.gov.uk/details/developers-guide/generic-api
- 'logging_level'
   - Can be set to either 'INFO' or 'ERROR'.

##### **Central panel**
The central panel of the interface displays the title and provides the user with quantative data figures on the number of hospital cases, cumulative deaths and the local and national seven day infection rate. The central panel also allows the user to schedule updates to occur, refreshing the webpage at specified times and updating either or both the covid data and news articles.
- This is acomplished by:
    - choosing time for the update to occur at from a 24 hour clock in the large central box
    - Setting the title of the update in the update label box 
    - checking the 'repeat update' checkbox if you wish the update to repeat regularly 
    - checking the 'update covid data' checkbox if you want to be updated 
    - checking the 'update news articles' checkbox if you want the news to be updated 


A new update can not be scheduled if an existing update of that name exists.

##### **Right panel**
The right panel of the interface provides the user with a list of news articles related to specifed terms. The terms in this case are related to covid-19 and therefore display headline articles from many different sources. Once an article has been read or if it doesn't catch the users attention it can be removed from the interface by clicking the cross in the top right corner of the article box. Removing an article will refresh the page with new articles. A max of 5 articles are displayed at a time. If all articles have been removed the interface displays a box where the articles would be notifying the user of this.

##### **Left panel**
The left panel of the interface provides ther user with a list of scheduled updates; created in the central panel. These scheduled updates provide information on the title of the udpate, the time it is scheduled for, whether it is repeatable and the content scheduled to be updated. Each scheduled update can be cancelled and removed from the interface by clicking the cross in the top right corner of the box. If there are no scheduled updates, the interface displays a box where the scheduled updates would be notifying the user of this.



## **Testing** 
The code can be executed from the main app.py module and can be tested by going to http://127.0.0.1:5000/ to see if the website is being hosted locally. 
Once on the interface, the news article side of the interface can be tested by closing some of the articles and seeing new articles brought up. The central interface can be tested by entering a time, label and selecting the desired checkboxes then waiting for it to appear on the scheduled updates list. After that time has occured, reloading the page will result in the update being removed from the scheduled updates list and the data selcted being updated. Unless the update was set to repeat in which case it will persist in the list. 

To test that the authentication of an update is correctly working an update of the same name can be attempted to be scheduled and should not appear in the scheduled update list. 

## **Developer Documentation**
Can be found by opening 'index.html' in a web browser. 

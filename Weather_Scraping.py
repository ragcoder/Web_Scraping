# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:46:25 2019

@author: RagCoder
Source: https://www.dataquest.io/blog/web-scraping-tutorial-python/
"""
'''Navigating a web page'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

#Retrieves web page from server
page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")

#parsing document
soup = BeautifulSoup(page.content, 'html.parser')

#Selecting tag with 7-day forecast
seven_day = soup.find(id="seven-day-forecast")

#Extracting all elements with class tombstone-container which holds the the days weather information
forecast_items = seven_day.find_all(class_="tombstone-container")

#Selecting today's forecast information
today = forecast_items[0]

print(today.prettify())

#Extracting time period, short description, and temperature
period = today.find(class_="period-name").get_text()
short_desc = today.find(class_="short-desc").get_text()
temp = today.find(class_="temp").get_text()

print(period)
print(short_desc)
print(temp)

#Extract img information
img = today.find("img")
desc = img['title']
print(desc)

#Extracting all information from page
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
print(periods)

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d['title'] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)

#Collecting and Analyzing
weather = pd.DataFrame({
        "period": periods,
        "short_desc": short_descs,
        "temp": temps,
        "desc": descs
        })
print(weather)

temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
print(temp_nums)
print("the average temp for this week: ", weather["temp_num"].mean())

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print(is_night)

print(weather[is_night])
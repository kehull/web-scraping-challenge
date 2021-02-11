from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.marsdb
collection = db.articles


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":"/Users/kelly/Downloads/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # SCRAPE ARTICLES
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find('div',class_="slide")
    news_title = results.find("div", class_="content_title").text
    news_p = results.find('div', class_='rollover_description_inner').text

    # SCRAPE FEATURED IMAGE
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2) 
    html = browser.html
    soup = bs(html, 'html.parser')
    header = soup.find('div', class_='header')
    image = header.find('img', class_='headerimage fade-in')
    img = image['src']
    relative_image_path = img
    url3 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    img_path = url3 + relative_image_path
    print(img_path)

    # SCRAPE FACTS TABLE
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df_html = df.to_html()

    # SCRAPE HEMISPHERES
    # will do later if i have time

    # STORE DATA IN DICTIONARY
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "img_path": img_path,
        "df_html": df_html
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

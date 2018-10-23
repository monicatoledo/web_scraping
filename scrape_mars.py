
# coding: utf-8
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from selenium import webdriver 


# In[2]:

def scrape():
    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    #get_ipython().system('which chromedriver')


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # # Mission to Mars
    # ### Step 1 - scraping 

    # ## NASA Mars News


    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # get the latest news title and paragraph
    news_title = soup.find("div", class_="content_title").get_text()
    news_par = soup.find("div", class_="article_teaser_body").get_text()

    news_data= {}
    news_data["news_title"] = news_title
    news_data["paragraph_1"] = news_par


    # ## JPL Mars Space Images - Featured Image


    #navigate the site and find the image url for the current Featured Mars Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    featured_image = soup.find("article", class_ = "carousel_item").get('style')


    featured_image_text = []
    featured_image_text= featured_image.split("'")
    featured_image_text=featured_image_text[1].split("'")


    featured_image_url= "https://www.jpl.nasa.gov"+featured_image_text[0]
    #print(featured_image_url)



    # ## Mars Weather

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    #print(tweet)



    # ## Mars Facts

    facts_url= "https://space-facts.com/mars/"

    tables = pd.read_html(facts_url)

    df= tables[0]

    html_table = df.to_html(header=False, index= False)
    #print(html_table)

    # ## Mars Hemispheres

    base= 'https://astrogeology.usgs.gov'
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url) 
    usgs_html = browser.html                                                     
    usgs_soup = BeautifulSoup(usgs_html, 'html.parser')


    hemisphere_image_urls = []                                                  
    products = usgs_soup.find('div', class_='result-list')                       
    hemispheres = products.find_all('div', class_='item')                        

    for hemisphere in hemispheres:                                               
        title = hemisphere.find('div', class_='description')                                       
        #title = hemisphere.a
        title_text = title.a.text 
        title_link = title.a.get('href')
        url= base + title_link
        browser.visit(url) 
        hem_html = browser.html                                                 
        hem_soup = BeautifulSoup(hem_html, 'html.parser')                               
        
        image = hem_soup.find('div', class_='downloads').find('ul').find('li')  
        img_url = image.a['href']
        
        hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})   
        
        browser.click_link_by_text('Back') 

    #print(hemisphere_image_urls)


    mars_data = {}

    mars_data["news_data"] = news_data

    mars_data["featured_image_url"] = featured_image_url

    mars_data["mars_weather"] = tweet

    mars_data["mars_facts"] = html_table

    mars_data["mars_hemispheres"] = hemisphere_image_urls

 # return mars_data dict
    return mars_data

#if __name__ == "__main__":
#    print(scrape())
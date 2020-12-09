from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import re
import time

def scrape():

    #We are installing the webdriver (robot)
    executable_path = {"executable_path": ChromeDriverManager().install()}
    #Splinter is creating a browser window with the robot
    browser = Browser("chrome", **executable_path, headless=False)

#NASA MARS NEWS
    browser.visit("https://mars.nasa.gov/news/")
    time.sleep(1)

    # Scrape page into Soup
    soup_Mars_News = bs(browser.html, 'html.parser')

    news_title = []
    news_p = []
    mars = {}

    #iterating to get the title from the beautiful soup object
    news = soup_Mars_News.find_all("div", class_="bottom_gradient")
    for n in news:
        news_title.append(n.text)

    #iterating to get the paragraph from the beautiful soup object
    news = soup_Mars_News.find_all("div", class_="article_teaser_body")
    for n in news:
        news_p.append(n.text)

    #populating dictionary with only the first item
    mars["news_title"]= news_title[0]
    mars["news_p"]= news_p[0]
    
#JPL MARMS SPACE IMAGES - FEATURE IMAGE
    # Scrape page into Soup
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    time.sleep(2)
    browser.find_by_id("full_image").click()
    time.sleep(2)
    browser.links.find_by_partial_text("more info").click() #find_link_by_partial_text
    time.sleep(2)
    soup_mars_images = bs(browser.html, 'html.parser')
    result = soup_mars_images.find("figure", class_="lede").a.img["src"]
    result =f'https://www.jpl.nasa.gov{result}'
    #Populating dictionary with large feature image 
    mars["featured_image"]=result

#MARS WEATHER - TWITTER
    #For some reason I need to shut dwon the bowser before scrapping twitter in order for this code to work
    browser.quit()
    #We are installing the webdriver (robot)
    executable_path = {"executable_path": ChromeDriverManager().install()}
    #Splinter is creating a browser window with the robot
    browser = Browser("chrome", **executable_path, headless=False)
    #Visiting twitter page
    browser.visit("https://twitter.com/marswxreport?lang=en")
    time.sleep(20)
    browser.execute_script("window.scrollTo(2, document.body.scrollHeight);")
    time.sleep(5)

    # Scrape page into Soup
    soup_tweet = bs(browser.html, 'html.parser')
    mars_weather = soup_tweet.find('span', text=re.compile('^InSight sol')) # 
    #Populating dictionary with weather tweet     
    mars["weather"]=mars_weather.string
    
#MARS FACTS
    url = 'https://space-facts.com/mars/'
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    tables = pd.read_html(url)
    #Table1 referes to Mars facts
    table1 = tables[0]
    table1.columns = ['Fact', 'Value']
    table1.set_index('Fact', inplace=True)
    html_table1 = table1.to_html()
    #Populating dictionary with Mars Facts
    mars["facts"]=html_table1

    #Table 2 referes to mars-earts comparisson
    table2 = tables[1]
    table2.rename(columns={'Mars - Earth Comparison': 'Facts'}, inplace=True)
    table2.set_index('Facts', inplace=True)

#MARS HEMISPHERES
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    time.sleep(1)
    soup_hemispheres = bs(browser.html, 'html.parser')
    #Getting the titles of the hemispheres from h3 tag
    hem_title = soup_hemispheres.find_all('h3')
    for x in range(0, len(hem_title)):
        hem_title[x]= hem_title[x].text

    dict={}
    dict['title'] = []
    dict['img_url'] = []
    c=0
    hem_url=[]

    for titulo in hem_title:
        hemispheres={}
        browser.links.find_by_partial_text(titulo).click()
        soup_hd_img = bs(browser.html, 'html.parser')
        hd_img = soup_hd_img.find('a', target="_blank", text=('Sample')).get('href')
        hemispheres['title']= titulo
        hemispheres['img_url']= hd_img
        hem_url.append(hemispheres)
        browser.back()
        c=c+1
    mars['hemispheres']=hem_url

# CLOSE THE BORWSER AFTER SCRAPING
    browser.quit()

# RETURN RESULTS
    return mars

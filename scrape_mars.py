# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time



def init_browser():
    executable_path = {"executable_path": "c:/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    # scrape the NASA Mars News Site 
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    time.sleep(5)

    # create beautiful soup object; parse with html.parser
    soup = bs(html, 'html.parser')

    # collect latest news title and paragraph text
    article = soup.find('div', class_='list_text')
    title = article.find('div', class_="content_title").get_text()
    paragraph = article.find('div', class_="article_teaser_body").get_text()


    mars['title'] = title
    mars['paragraph'] = paragraph

    # scrape the JPL featured space image
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)
    time.sleep(10)

    # go to the full image
    browser.find_by_xpath('/html/body/div/div/div[3]/section[1]/div/div/article/div[1]/footer/a').click()
    browser.click_link_by_partial_text('more info')

    # parse html 
    html = browser.html
    featured_soup = bs(html, 'html.parser')

    # scrape the image from the url
    img = featured_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{img}'
    print(featured_image_url)

    mars['featuredimage'] = featured_image_url

    # use pandas to scrape mars facts re: diameter, mass, etc.
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # get tables from the webpage
    tables = pd.read_html(facts_url)

    # save the first table as a dataframe
    mars_df = tables[0]

    # rename the columns
    mars_df.columns = ['Description', 'Mars']

    # set hte first column as the index
    mars_df.set_index('Description', inplace=True)


    # convert data to html table
    html_mars_table = mars_df.to_html()

    # clean up html table formatting
    html_mars_table.replace('\n', '')
    mars['table'] = html_mars_table

    # scrape high resolution images for each hemisphere along with hemisphere title
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemisphere_url)

    # navigate to the cerberus hemisphere page and get the URL of the high resolution image
    browser.click_link_by_partial_text('Cerberus')

    html = browser.html
    hem_soup = bs(html, 'html.parser')

    # find and save the URL for cerberus hemisphere
    cerb_img = hem_soup.find('img', class_='wide-image')['src']
    cerb_url = f'https://astrogeology.usgs.gov{cerb_img}'

    # return to the main page
    browser.back()

    # schiaparelli hemisphere
    # navigate to the schiaparelli hemisphere page and get the URL of the high resolution image
    browser.click_link_by_partial_text('Schiaparelli')

    html = browser.html
    hem_soup = bs(html, 'html.parser')

    # find and save the URL for cerberus hemisphere
    schiap_img = hem_soup.find('img', class_='wide-image')['src']
    schiap_url = f'https://astrogeology.usgs.gov{schiap_img}'

    # syrtis major hemisphere
    # return to the main page
    browser.back()

    # navigate to the schiaparelli hemisphere page and get the URL of the high resolution image
    browser.click_link_by_partial_text('Syrtis Major')

    html = browser.html
    hem_soup = bs(html, 'html.parser')

    # find and save the URL for cerberus hemisphere
    sm_img = hem_soup.find('img', class_='wide-image')['src']
    sm_url = f'https://astrogeology.usgs.gov{sm_img}'

    # valles marineris hemisphere
    # return to the main page
    browser.back()

    # navigate to the schiaparelli hemisphere page and get the URL of the high resolution image
    browser.click_link_by_partial_text('Valles')

    html = browser.html
    hem_soup = bs(html, 'html.parser')

    # find and save the URL for cerberus hemisphere
    vm_img = hem_soup.find('img', class_='wide-image')['src']
    vm_url = f'https://astrogeology.usgs.gov{vm_img}'

    # store in python dictionary using img_url and title.
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": vm_url},
        {"title": "Cerberus Hemisphere", "img_url": cerb_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schiap_url},
        {"title": "Syrtis Major Hemisphere", "img_url": sm_url},
    ]

    mars['hemispheres'] = hemisphere_image_urls

    return mars
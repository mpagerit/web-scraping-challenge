{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies\n",
    "from bs4 import BeautifulSoup as bs\n",
    "from splinter import Browser\n",
    "import pandas as pd\n",
    "import requests\n",
    "import time\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def init_browser():\n",
    "    executable_path = {\"executable_path\": \"c:/bin/chromedriver\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "browser = init_browser()\n",
    "\n",
    "# scrape the NASA Mars News Site \n",
    "news_url = 'https://mars.nasa.gov/news/'\n",
    "browser.visit(news_url)\n",
    "html = browser.html\n",
    "# time.sleep(2)\n",
    "\n",
    "# create beautiful soup object; parse with html.parser\n",
    "soup = bs(html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# collect latest news title and paragraph text\n",
    "article = soup.find('div', class_='list_text')\n",
    "title = article.find('div', class_=\"content_title\").get_text()\n",
    "paragraph = article.find('div', class_=\"article_teaser_body\").get_text()\n",
    "\n",
    "print(title)\n",
    "print(paragraph)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape the JPL featured space image\n",
    "JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "browser.visit(JPL_url)\n",
    "time.sleep(2)\n",
    "\n",
    "# go to the full image\n",
    "browser.find_by_xpath('/html/body/div/div/div[3]/section[1]/div/div/article/div[1]/footer/a').click()\n",
    "\n",
    "browser.click_link_by_partial_text('more info')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# parse html \n",
    "html = browser.html\n",
    "featured_soup = bs(html, 'html.parser')\n",
    "\n",
    "# scrape the image from the url\n",
    "img = featured_soup.find('figure', class_='lede').a['href']\n",
    "featured_image_url = f'https://www.jpl.nasa.gov{img}'\n",
    "print(featured_image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# use pandas to scrape mars facts re: diameter, mass, etc.\n",
    "facts_url = 'https://space-facts.com/mars/'\n",
    "browser.visit(facts_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# get tables from the webpage\n",
    "tables = pd.read_html(facts_url)\n",
    "\n",
    "# save the first table as a dataframe\n",
    "mars_df = tables[0]\n",
    "\n",
    "# set hte first column as the index\n",
    "mars_df.set_index(0, inplace=True)\n",
    "\n",
    "mars_df.head()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# convert data to html table\n",
    "html_mars_table = mars_df.to_html()\n",
    "\n",
    "# clean up html table formatting\n",
    "html_mars_table.replace('\\n', '')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape high resolution images for each hemisphere along with hemisphere title\n",
    "hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "\n",
    "browser.visit(hemisphere_url)\n",
    "\n",
    "# navigate to the cerberus hemisphere page and get the URL of the high resolution image\n",
    "browser.click_link_by_partial_text('Cerberus')\n",
    "\n",
    "html = browser.html\n",
    "hem_soup = bs(html, 'html.parser')\n",
    "\n",
    "# find and save the URL for cerberus hemisphere\n",
    "cerb_img = hem_soup.find('img', class_='wide-image')['src']\n",
    "cerb_url = f'https://astrogeology.usgs.gov{cerb_img}'\n",
    "\n",
    "# print to verify\n",
    "print(cerb_url)\n",
    "\n",
    "# return to the main page\n",
    "browser.back()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# schiaparelli hemisphere\n",
    "\n",
    "# navigate to the schiaparelli hemisphere page and get the URL of the high resolution image\n",
    "browser.click_link_by_partial_text('Schiaparelli')\n",
    "\n",
    "html = browser.html\n",
    "hem_soup = bs(html, 'html.parser')\n",
    "\n",
    "# find and save the URL for cerberus hemisphere\n",
    "schiap_img = hem_soup.find('img', class_='wide-image')['src']\n",
    "schiap_url = f'https://astrogeology.usgs.gov{schiap_img}'\n",
    "\n",
    "# print to verify\n",
    "print(schiap_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# syrtis major hemisphere\n",
    "\n",
    "# return to the main page\n",
    "browser.back()\n",
    "\n",
    "# navigate to the schiaparelli hemisphere page and get the URL of the high resolution image\n",
    "browser.click_link_by_partial_text('Syrtis Major')\n",
    "\n",
    "html = browser.html\n",
    "hem_soup = bs(html, 'html.parser')\n",
    "\n",
    "# find and save the URL for cerberus hemisphere\n",
    "sm_img = hem_soup.find('img', class_='wide-image')['src']\n",
    "sm_url = f'https://astrogeology.usgs.gov{sm_img}'\n",
    "\n",
    "# print to verify\n",
    "print(sm_url)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# valles marineris hemisphere\n",
    "\n",
    "# return to the main page\n",
    "browser.back()\n",
    "\n",
    "# navigate to the schiaparelli hemisphere page and get the URL of the high resolution image\n",
    "browser.click_link_by_partial_text('Valles')\n",
    "\n",
    "html = browser.html\n",
    "hem_soup = bs(html, 'html.parser')\n",
    "\n",
    "# find and save the URL for cerberus hemisphere\n",
    "vm_img = hem_soup.find('img', class_='wide-image')['src']\n",
    "vm_url = f'https://astrogeology.usgs.gov{vm_img}'\n",
    "\n",
    "# print to verify\n",
    "print(vm_url)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# store in python dictionary using img_url and title.\n",
    "\n",
    "hemisphere_image_urls = [\n",
    "    {\"title\": \"Valles Marineris Hemisphere\", \"img_url\": vm_url},\n",
    "    {\"title\": \"Cerberus Hemisphere\", \"img_url\": cerb_url},\n",
    "    {\"title\": \"Schiaparelli Hemisphere\", \"img_url\": schiap_url},\n",
    "    {\"title\": \"Syrtis Major Hemisphere\", \"img_url\": sm_url},\n",
    "]"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

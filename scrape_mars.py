from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from selenium import webdriver
import cssutils
import time
# url = "https://mars.nasa.gov/news/"
final_dct = {}

# must do first part

def scrape():
    # Get latest news title and text
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')
    # print(soup.prettify())
    content_title_div = soup.find('div', class_='list_text')
    news_title = content_title_div.find('div', class_='content_title').a.text
    news_p = content_title_div.find('div', 'article_teaser_body').text
    final_dct['news_title'] = news_title
    final_dct['news_p'] = news_p
    final_dct
    
    # Get featured img url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    browser.click_link_by_id("full_image")
    time.sleep(10)
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('img', class_='fancybox-image')
    img_src = img['src']
    featured_image_url = 'https://www.jpl.nasa.gov' + img_src
    final_dct["featured_img_url"] = featured_image_url

    # Get Mars data table
    url = "https://space-facts.com/mars/"
    d = pd.read_html(url)
    df = pd.DataFrame({})
    df['Attribute'] = d[1]['Mars - Earth Comparison']
    df['Mars'] = d[1]['Mars']
    table_html = df.to_html()
    final_dct['table_html'] = table_html


    # Get hemisphere title and img url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    links = browser.find_link_by_partial_href('enhanced')
    final_links = []
    for i in links:
        if final_links.count(i['href']) == 0:
            final_links.append(i['href'])
        else:
            pass
    hemisphere_img_urls = []
    main_url = 'https://astrogeology.usgs.gov'
    for i in final_links:
        browser.visit(i)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find('img', class_='wide-image')
        img_src = img['src']
        img_url = main_url + img_src
        hemisphere_title = soup.find('h2', class_='title').text
        final_title = hemisphere_title.rsplit(' ', 1)[0]
        hemisphere_img_urls.append({
            "title": final_title,
            "img_url": img_url
        })
    final_dct['hemisphere_img_urls'] = hemisphere_img_urls

    return final_dct

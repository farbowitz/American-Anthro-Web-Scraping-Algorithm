# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 22:24:05 2021

@author: Daniel

Dependencies: bs4, html5lib, pandas, selenium
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

#LVL 0: Call up initial page
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

site_prefix = 'https://anthrosource.onlinelibrary.wiley.com/loi/15481433/'
driver.get(site_prefix)


#LVL 1: Open all year pages
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
all_links = [link['href'] for link in soup.findAll("a")]
loi_links = []
for item in all_links:
    if '/loi' and 'year' in item:
        loi_links.append(item[1:])
driver.quit()
#LVL 2: Access each journal
### If permalist not found, occupy it
PERM_URLS = []
for item in loi_links:
    driver = webdriver.Firefox(options=options)
    driver.get(site_prefix+item)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls = [data['href'] for data in soup.find_all('a', class_='visitable')]
    PERM_URLS.extend(urls)
print(PERM_URLS)

    
    
    #LVL3: Get info from each journal
    for url in urls:
        driver.get('https://anthrosource.onlinelibrary.wiley.com'+url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('div', class_='issue-item')
        for article in articles:
            title = article.h2.get_text()
            print(title)
            authors = article.find_all(attrs={'class':'author-style'})
            for author in authors:
                print(author.get_text())
            date = article.find_all(attrs={'class':'ePubDate'})[-1].get_text().split(':')[1]
            print(date)
            abstract = soup.find_all('div', class_='toc-item__abstract abstract-preview')
            print(abstract)
    driver.quit()

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 22:24:05 2021

@author: Daniel

Dependencies: bs4, html5lib, pandas, selenium, os
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.firefox.options import Options


#input info
site_prefix = 'https://anthrosource.onlinelibrary.wiley.com/loi/15481433/'
file_name = 'JOURNAL_URLs.txt'

"""


def populate_list(prefix = site_prefix, file_name = file_name):
    #LVL 1: Open all years 
    options = Options()
    
    ##run browser without opening visible window
    options.headless = True
    
    ##read html using firefox browser NOTE:'geckodriver' must be installed in working directory/PATH
    driver = webdriver.Firefox(options=options)
    driver.get(prefix)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    ##find all links on summary page
    all_links = [link['href'] for link in soup.findAll("a")]
    ###populate list with appropriate link styles for individual years
    loi_links = []
    for item in all_links:
        if '/loi' and 'year' in item:
            loi_links.append(item[1:])
    ##browser quit
    driver.quit()
    
    #LVL 2: Access each journal
    ### Create list of URLs to save to file
    url_list = []
    print('Populating List...')
    for item in loi_links:
        ###open browser and get HTML
        driver = webdriver.Firefox(options=options)
        driver.get(site_prefix+item)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        ###get all individual journal issue links
        url_list.extend([data['href'] for data in soup.find_all('a', class_='visitable')])
        print('.')
        driver.quit()
        
    ##Save URL_list to file
    textfile = open(file_name, "w+")
    for element in url_list:
        textfile.write(element + "\n")
    textfile.close()
    
    ##check if URL_list is correct
    return print(url_list)


def individual_article_info(soup, volume, issue, year, section, subsection):
     #Define list of dictionaries that will form eventual pandas dataframe
     rows_list =[]
     articles = soup.find_all('div', class_='issue-item')
     for article in articles:
         title = article.h2.get_text()
         authors = article.find_all(attrs={'class':'author-style'})
         author_list = ''
         for author in authors:
            if author_list == '':
                author_list += author.get_text().strip()     
            else:
                author_list += '; ' + author.get_text().strip() 
         date = article.find_all(attrs={'class':'ePubDate'})[-1].get_text().split(':')[1]
         abstract = article.find_all('div', class_='toc-item__abstract abstract-preview')
         pages = article.find_all(attrs={'class':'page-range'})[-1].get_text().split(':')[1]
         
         pdf_link = [data['href'] for data in article.find_all('a', title='EPDF')][0]
         dict1 = {'Title':title, 'Author(s)':author_list, 'Year':year, 'Date':date, 'Pages':pages, 'Volume':volume, 'Issue':issue, 'Section':section, 'Subsection':subsection,'Abstract':abstract, 'Access URL':pdf_link}
         rows_list.append(dict1)
     df = pd.DataFrame(rows_list, columns = ['Title', 'Author(s)', 'Date', 'Year', 'Pages', 'Volume', 'Issue', 'Section', 'Subsection', 'Abstract', 'Access URL'])
     print(df)
     return df



def nesting_doll(url_suffix):
    dataframes = []
    
    #Take info availale from URL suffix
    meta = url_suffix.split(sep='/')
    volume = meta[-2]
    issue = meta[-1]
    year = meta[-3]
    
    #run browser without opening visible window
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://anthrosource.onlinelibrary.wiley.com'+url_suffix)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    #Working inwards - find each section heading
    secs = soup.find_all('div', class_='issue-items-container bulkDownloadWrapper')
    if secs:
        for sec in secs:
            section = sec.find(attrs={'class':'toc__heading section__header to-section'}).get_text()
            #check children of section to see if there is subsection or not
            if sec.descendants.has_attr('h4'):
                for child in sec.children:
                    subsec = child.find_all('div', class_='issue-item')
                    subsection = subsec.h4.get_text()
                    for subchild in subsec.children:
                        dataframes.append(individual_article_info(subchild, volume, issue, year, section, subsection))
            else:
                subsection=''
                dataframes.append(individual_article_info(sec, volume, issue, year, section, subsection))
    else:
        section = ''
        subsection = ''
        dataframes.append(individual_article_info(soup, volume, issue, year, section, subsection))
    return pd.concat(dataframes)




#Method A: Populate List of URLs, then scrape them


if (not os.path.exists(file_name)) or (os.stat(file_name).st_size() == 0):
    populate_list(site_prefix, file_name)

with open(file_name, "r") as f:
    url_list = f.read().splitlines()
big_df = pd.concat([nesting_doll(url) for url in url_list])
print(big_df)
    

#Method B: Do everything at once  
"""

#trying outstuff
with open(file_name, "r") as f:
    url_list = f.read().splitlines()
dataframes = []

def cat(soup, tag, class_identifier):
    if soup.find(tag, class_=class_identifier):
        return soup.find(tag, class_=class_identifier).get_text().strip()
    else:
        return ""

def individual_article_info(article, volume, issue, year, section, subsection):
     #Define list of dictionaries that will form eventual pandas dataframe
     titl = title(article, 'h2')
     authors = article.find_all(attrs={'class':'author-style'})
     author_list = ''
     for author in authors:
         if author_list == '':
            author_list += author.get_text().strip()     
         else:
            author_list += '; ' + author.get_text().strip() 
     date = article.find_all(attrs={'class':'ePubDate'})[-1].get_text().split(':')[1]
     abstract = cat(article, 'div', 'toc-item__abstract abstract-preview')
     pages = article.find_all(attrs={'class':'page-range'})[-1].get_text().split(':')[1]
     pdf_link = [data['href'] for data in article.find_all('a', title='EPDF')][0]
     return {'Title':titl, 'Author(s)':author_list, 'Year':year, 'Date':date, 'Pages':pages, 'Volume':volume, 'Issue':issue, 'Section':section, 'Subsection':subsection,'Abstract':abstract, 'Access URL':pdf_link}

    
     
 
def title(soup,class_attribute):
    #first check for existence
    if soup.find(class_attribute):
        return soup.find(class_attribute).get_text().strip()
    else:
        return ""

    




"""
#Working inwards - find each section heading
secs = soup.find_all('div', class_='issue-items-container bulkDownloadWrapper')
if secs:
    for sec in secs:
        section = sec.find(attrs={'class':'toc__heading section__header to-section'}).get_text()
        #check children of section to see if there is subsection or not
        print(sec.parent)
        i=0
        print(sec.find('h4'))
        if i>0:
            for child in sec.children:
                subsec = child.find_all('div', class_='issue-item')
                subsection = subsec.h4.get_text()
                for subchild in subsec.children:
                    dataframes.append(individual_article_info(subchild, volume, issue, year, section, subsection))
        else:
            subsection=''
            dataframes.append(individual_article_info(sec, volume, issue, year, section, subsection))
else:
    section = ''
    subsection = ''
    dataframes.append(individual_article_info(soup, volume, issue, year, section, subsection))
"""
#working outwards
def outward_scan(url_suffix):
    #Take info availale from URL suffix
    meta = url_suffix.split(sep='/')
    volume = meta[-2]
    issue = meta[-1]
    year = meta[-3]
    
    
    options = Options()
    #run browser without opening visible window
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://anthrosource.onlinelibrary.wiley.com'+url_suffix)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(url_suffix)
    
    items = soup.find_all('div', class_='issue-item')
    rows_list = []
    for item in items:
   
        #silly method perhaps, but checking if 'issue-item' in question is actually subsection
        i=0
        for child in item.children:
            if '<h4>' in child:
                i+=1
        #issues w/sections but not subsections
        if ('issue-items-container' in item.parent['class']) and (i==0):
            section = title(item.parent, 'h3')
            #check item is not a subsection
            subsection = ""
            rows_list.append(individual_article_info(item, volume, issue, year, section, subsection))
        #issue w/sections and subsections    
        elif 'issue-item' in item.parent['class']:
            section = title(item.parent.parent, 'h3')
            subsection = title(item.parent, 'h4')
            rows_list.append(individual_article_info(item, volume, issue, year, section, subsection))
        else:
            print('wonky one')
            section = ''
            subsection = ''
            rows_list.append(individual_article_info(item, volume, issue, year, section, subsection))
            
    print('...')
    df = pd.DataFrame(rows_list, columns = ['Title', 'Author(s)', 'Date', 'Year', 'Pages', 'Volume', 'Issue', 'Section', 'Subsection', 'Abstract', 'Access URL'])
    print(df)
    driver.quit()
    return df
dataframes = [outward_scan(url) for url in url_list]
big_df = pd.concat(dataframes)
big_df.to_excel('compiled_catalog_AA.xlsx')
                                

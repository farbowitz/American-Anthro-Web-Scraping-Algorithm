# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:36:05 2022

@author: Daniel

Downloader for AA files
"""

#API/JSON interface
import requests
import json

#working with home folders
import os

#time for spacing requests
import time
#pandas to read csv
import pandas as pd

#get rid of the damn double quote
from unidecode import unidecode
import string

#set working directory
wd = 'C:/Users/Daniel/Desktop/Programming/AA Project/'
os.chdir(wd)


ref_csv = 'compiled_catalog_AA.xlsx - Publication Dataset.csv'
container = 'Journal Articles/'
user_token = '04256682-ec15-4c49-81f7-624b452e80ea'

#GET URLS from file, which contain DOIs
df = pd.read_csv(ref_csv)
df_URLs = df['Access URL']
df['File Formatted Name'] = 'Vol '+df['Volume'] +' Iss '+df['Issue']+' -- '+df['Author(s)']+' -- '+df['Title']
#remove all goddamn punctuation
df['File Formatted Name'] = df['File Formatted Name'].apply(lambda x: unidecode(str(x)).translate(str.maketrans('', '', string.punctuation))+'.pdf')
df_names = df['File Formatted Name']


#putting together DOI
def doi_from_url(url):
    doi = url.split(sep='/')
    doi = '/'.join(doi[-2:])
    return doi

'''
#Getting metadata from http://dx.doi.org
headers = {
    'Accept': 'application/vnd.crossref.unixsd+xml',
}

response = requests.get('http://dx.doi.org/10.1111/aman.13633', headers=headers)
#data = json.load(response.text)
print(response.text)
'''

#Liz is busy so let's try just doing this with selenium

#FUCK OFF WILEY YOU SHITBAG




#function for each request
def download_pdf(doi, name, token = user_token):
    
    headers = {
        'Wiley-TDM-Client-Token': token,
        }
    #start a session
    s = requests.Session()

    #add headers to session
    s.headers.update(headers)
    standard_address = 'https://api.wiley.com/onlinelibrary/tdm/v1/articles/'+doi.replace('/', '%2F')
    print(standard_address)
    response = s.get(standard_address, headers=headers, allow_redirects=True)
    print(response.status_code)
    print(response.headers)
    #print(response.content)
    with open(wd+"Journal Articles/"+name, 'wb') as f:
        f.write(response.content)
    time.sleep(3)

#ex url: https://onlinelibrary.wiley.com/doi/10.1111/aman.13383
#https://api.wiley.com/onlinelibrary/tdm/v1/articles/10.1525%2Faa.1889.2.4.02a00060
'''
for index in range(len(df)):
    url = df_URLs.loc[index]
    #remove any quotes from names so as not to throw an error
    name = df_names.loc[index].replace('"', '')
    print(name)
    doi = doi_from_url(url)
    print(doi)
    download_pdf(doi, name)
#are some of them just freely available and the token doesn't work?
'''
#ONCE AGAIN< FUCK OFF WILEY

#MUST CREATE FOLDER FOR EACH PDF SO pyResearchInsights can print to that folder... OR change how it labels its outputs??

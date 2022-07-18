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

#set working directory
wd = 'C:/Users/Daniel/Desktop/Programming/AA Project/'
os.chdir(wd)


ref_csv = 'compiled_catalog_AA.xlsx - Publication Dataset.csv'
container = 'Journal Articles/'
user_token = '4bc11424-eb07-4d05-b137-2ead3b257a38'

#GET URLS from file, which contain DOIs
df = pd.read_csv(ref_csv)
df_URLs = df['Access URL']

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
def download_pdf(doi, token = user_token):
    s = requests.Session()
    res = s.get('https://onlinelibrary.wiley.com')
    headers = {
        'Wiley-TDM-Client-Token': token,
        }
    cookies = dict(res.cookies)
    response = requests.request('GET','https://onlinelibrary.wiley.com/doi/pdf/'+doi, headers=headers, cookies = cookies, allow_redirects=True)
    print(response.text)
    print(response.headers)
    print(response.content)
    with open('12168.pdf', 'wb') as f:
        f.write(response.content)



#MUST CREATE FOLDER FOR EACH PDF SO pyResearchInsights can print to that folder... OR change how it labels its outputs??

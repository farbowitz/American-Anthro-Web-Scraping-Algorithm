# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 14:50:27 2022

@author: Daniel
"""


import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

file_name = "C:/Users/Daniel/Downloads/compiled_catalog_AA.xlsx - Publication Dataset.csv"
download_folder = "C:/ProgramData/Miniconda3/Scripts/AA_pdf_files_for_NLP/Test"
df = pd.read_csv(file_name)
print(df.columns)
url = 'https://anthrosource.onlinelibrary.wiley.com/doi/epdf/10.1111/aman.13633'




options = Options()
options.headless = False

options.set_preference("browser.download.dir", download_folder)

driver = webdriver.Firefox(options=options)


driver.get(url)





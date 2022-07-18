# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 23:37:42 2021

@author: Daniel
"""

from tika import parser
file = r'C:\Users\Daniel\Downloads\2108.01681.pdf'
file_data = parser.from_file(file)
text = file_data['content']
print(text)

from pyResearchInsights.common_functions import pre_processing
from pyResearchInsights.Scraper import scraper_main
from pyResearchInsights.Cleaner import cleaner_main
from pyResearchInsights.Analyzer import analyzer_main
from pyResearchInsights.NLP_Engine import nlp_engine_main




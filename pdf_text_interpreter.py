# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:43:32 2022

@author: Daniel

text language interpreter
"""

import fitz # install using: pip install PyMuPDF #fitz is used in pdf_parser
#get text data from pdf_parser.py
from pdf_parser import return_text

containing_folder = 'C:/Users/Daniel/Desktop/Programming/AA Project/'

test_file = 'American Anthropologist - 2021 - Nelson - Where Have All the Anthros Gone The Shift in California Indian Studies from.pdf'

test_path = containing_folder+test_file





#Applying pyResearchInsights, a library designed around scraping abstracts under search terms
#create text file for pdf content
text_file = open(test_path+'.txt', "w")
 
#write string to file
text_file.write(return_text(test_path))
 
#close file
text_file.close()



#Importing the cleaner_main() to clean the txt file of abstracts
from pyResearchInsights.Cleaner import cleaner_main
from pyResearchInsights.Analyzer import analyzer_main
from pyResearchInsights.NLP_Engine import nlp_engine_main


#The location of the file to be cleaned is mentioned here
abstracts_log_name = test_path+'.txt'

#status_logger() logs the seequence of functions executed during the code run
status_logger_name = test_file

#Calling the main functions on the text file 
cleaner_main(abstracts_log_name, status_logger_name)
analyzer_main(abstracts_log_name, status_logger_name)
nlp_engine_main(abstracts_log_name, status_logger_name)

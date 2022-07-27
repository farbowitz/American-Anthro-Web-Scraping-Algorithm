# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:43:32 2022

@author: Daniel

text language interpreter
"""
from asyncio.log import logger
import logging
import fitz # install using: pip install PyMuPDF #fitz is used in pdf_parser
#get text data from pdf_parser.py
from pdf_parser import return_text
import pandas as pd

containing_folder = 'C:/Users/Daniel/Desktop/Programming/AA Project/'

term_file = 'Variable lookup - Definitions.csv'

test_file = 'American Anthropologist - June 1976 - PARKER - The Precultural Basis of the Incest Taboo Toward a Biosocial Theory.pdf'

test_path = containing_folder+test_file


logging.basicConfig()



#METHOD I: Applying pyResearchInsights, a library designed around scraping abstracts under search terms
def pRI(test_path):

    test_file = test_path.split(sep='/')[-1]

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

    #using test_file name in place of status logger so output files can be renamed within the same folder, adapted pyResearchInsights code slightly to allow this
    status_logger_name = test_file

    #Calling the main functions on the text file 
    cleaner_main(abstracts_log_name, status_logger_name)
    analyzer_main(abstracts_log_name, status_logger_name)
    nlp_engine_main(abstracts_log_name, status_logger_name)
    logger.info('Output complete.')



#pRI(test_path)


#NOTES

#METHOD II: SIMPLE SEARCH TERMS IN TEXT

df = pd.read_csv(containing_folder+term_file, header=34)
'''
all_words = df['Keywords'].str.split(expand=True).unstack().value_counts()
print(all_words)
'''

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import re

#EXTRA SIMPLE, BRUTE FORCE-Y Version
text = return_text(test_path)
def simple_keyword_counter(text):
    result = re.sub(r'[\.\?\!\,\:\;\"]', '', text)
    result = result.lower()
    text_tokenize = word_tokenize(result)
    print('Relevant words appearing in text {}:'.format(test_file))
    for keyword in df['Keywords']:
        count = 0
        phrase_len = len(keyword.split(sep=' '))
        phrase = keyword.lower()
        for index in range(len(text_tokenize)):
            guess = ' '.join(text_tokenize[index:index+phrase_len])
            if guess == phrase:
                count += 1
        if count > 0:
            print('{}: {} appearances'.format(phrase, count))
    return phrase, count

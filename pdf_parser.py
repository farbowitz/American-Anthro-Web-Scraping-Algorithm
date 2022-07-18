# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 09:06:51 2022

@author: Daniel

PDF parser using various libraries
"""



'''
###scipdf

#METHOD FAILED, can't figure out grobid bullshit
import scipdf
import subprocess

#call bash script
#subprocess.call('C:/ProgramData/Miniconda3/Scripts/serve_grobid.sh')


article_dict = scipdf.parse_pdf_to_dict('C:/Users/Daniel/Desktop/Programming/AA Project/American Anthropologist - June 1982 - FLANNERY - The Golden Marshalltown A Parable for the Archeology of the 1980s.pdf')

print(article_dict)

'''



'''

### tika

#METHOD SUCCESSFUL, too much time to remote to server though
# import parser object from tike
from tika import parser  
  
# opening pdf file
parsed_pdf = parser.from_file("C:/Users/Daniel/Desktop/Programming/AA Project/American Anthropologist - June 1982 - FLANNERY - The Golden Marshalltown A Parable for the Archeology of the 1980s.pdf")
  
# saving content of pdf
# you can also bring text only, by parsed_pdf['text'] 
# parsed_pdf['content'] returns string 
data = parsed_pdf['content'] 
  
# Printing of content 
print(data)
  
# <class 'str'>
print(type(data))
'''





'''

### Textract

#METHOD FAILED, textract is a load of shit
import textract
text = textract.process('C:/Users/Daniel/Desktop/Programming/AA Project/American Anthropologist - June 1982 - FLANNERY - The Golden Marshalltown A Parable for the Archeology of the 1980s.pdf', method='pdfminer')

print(text)
'''




'''
### PyPDF2

#METHOD SUCCESSFUL, needs some improvement in understanding scientific text, but the words are there
from PyPDF2 import PdfReader

reader = PdfReader("C:/Users/Daniel/Desktop/Programming/AA Project/American Anthropologist - June 1982 - FLANNERY - The Golden Marshalltown A Parable for the Archeology of the 1980s.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
print(text)
'''




### PyMuPDF
import fitz # install using: pip install PyMuPDF
#METHOD SUCCESSFUL, maybe slightly better than PyPDF2? About the same though
def return_text(file_path):



    with fitz.open(file_path) as doc:
        #print(doc.mjetadata) #metadata not super useful with old pdfs, only got title, no author
        #print(doc.load_page(1).get_text())
        text = ""
        for page in doc:
            text += page.get_text()
    return text



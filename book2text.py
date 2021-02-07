'''Uses os.walk to traverse a diverse the books directory and will convert
.epub, .pdf, and .mobi files into plain text. This script will not work on
 files that are DRM protected.'''


import sys
import os

import fitz
import mobi

from os import path

'''Converts a .epub file into a text file in the text directory using the
PyMuPDF library.'''
def epub_to_text(file_name):
    # parse the text from the file using PyMuPDF
    _, extension = os.path.splitext(file_name)
    _, name = os.path.split(file_name)

    try:
        doc = fitz.open(file_name)
        out = open(text_path + name + '.txt', 'wb')
        for page in doc:
            text = page.get_text('text').encode('utf-8')
            out.write(text)
            out.write(bytes((12,))) # page delimiter (form feed 0x0C)
        out.close()
        print(name + ' converted.')

    except RuntimeError as error:
        print(error)

'''Converts pdfs into text files in the text directory by calling the
epub_to_text function. This is seperated for possible future expansion if pdfs
end up needing special attention.'''
def pdf_to_txt(file_name):
    epub_to_text(file_name)

'''Converts mobis into text files in the text directory by decompressing them
with the mobi library and then parsing them with the PyMuPDF library.'''
def mobi_to_text(file_name):
    _, temp  = mobi.extract(file_name)
    _, extension = os.path.splitext(file_name)
    _, name = os.path.split(file_name)

    try:
        doc = fitz.open(temp)
        out = open(text_path + name + '.txt', 'wb')
        for page in doc:
            text = page.get_text('text').encode('utf-8')
            out.write(text)
            out.write(bytes((12,))) # page delimiter (form feed 0x0C)
        out.close()
        print(name + ' converted.')

    except RuntimeError as error:
        print(error)



# create a couple of global paths to be used by this script
current_path = os.getcwd()
books_path = os.path.join(current_path, 'books\\')
text_path = os.path.join(current_path, 'text\\')

# if the text directory doesn't exist, create it
if not os.path.isdir(text_path):
    os.mkdir(text_path)

# walk through the books directory and convert each file into a txt files
if os.path.isdir(books_path):
    for root, dirs, files in os.walk(books_path):
        for file in files:
            _, extension = os.path.splitext(file)
            file_name = os.path.join(root, file)
            if extension == '.epub':
                epub_to_text(file_name)
            elif extension == '.pdf':
                pdf_to_txt(file_name)
            elif extension == '.mobi':
                mobi_to_text(file_name)
            else:
                print('Error: ' + extension + ' filetype not supported.')

"""
File: PDF_RiskFinder_Extractor.py
Author: EC
Created: 2024-08-25

Description: 
The script uses natural language processing to identify and extract paragraphs related to risk from a PDF
Script can help to highlight recorded risks from Board and Annual Performance reports.

Sample report, Annual Report 2023 24
https://www.imperial.nhs.uk/about-us/how-we-are-doing/annual-reports

"""
#!pip install PyPDF2
#!pip install nltk

# Need this unzip command if using Kaggle
#!unzip /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora/

import PyPDF2
import re
import csv
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

pdf_path = '/kaggle/input/imperial-annual-report-202324/Annual Report 2023 24.pdf'

# Open in read binary mode
file = open(pdf_path,'rb')

reader = PyPDF2.PdfReader(file)

num_pages = len(reader.pages)

print(f'The pdf contains {num_pages} pages')

# Create a list of words associated with risk using WordNet
risk_synonyms = set()
for syn in wordnet.synsets('risk'):
    for lemma in syn.lemmas():
        risk_synonyms.add(lemma.name())

risk_synonyms = list(risk_synonyms)
#print(f'Words associated with "risk": {risk_synonyms}')

# Initialize the PorterStemmer
stemmer = PorterStemmer()

# Stemmer normalises words, stips off plural form or past tense
stemmed_risk_terms = [stemmer.stem(term) for term in risk_synonyms]

# Extract paragraphs containing risk related terms
def extract_risk_paragraphs(text, risk_terms):
    paragraphs = text.split('\n\n')
    risk_paragraphs = []
    for paragraph in paragraphs:
        # Stem the words in the paragraph
        stemmed_paragraph = ' '.join([stemmer.stem(word) for word in paragraph.split()])
        if any(term in stemmed_paragraph for term in risk_terms):
            risk_paragraphs.append(paragraph)
    return risk_paragraphs

# Extract text from each page and search for risk-related paragraphs
all_risk_paragraphs = []
for page_num in range(num_pages):
    page = reader.pages[page_num]
    text = page.extract_text()
    risk_paragraphs = extract_risk_paragraphs(text, stemmed_risk_terms)
    for paragraph in risk_paragraphs:
        all_risk_paragraphs.append((paragraph, page_num + 1))  # Store paragraph with page number

# Print the risk related paragraphs with page numbers
for i, (paragraph, page_num) in enumerate(all_risk_paragraphs):
    print(f'Paragraph {i+1} (Page {page_num}‡):')
    print(paragraph)
    print('\n')

# Export  paragraphs 
with open('risk_paragraphs.txt', 'w', encoding='utf-8') as f:
    for i, (paragraph, page_num) in enumerate(all_risk_paragraphs):
        f.write(f'Paragraph {i+1} (Page {page_num}‡)|{paragraph}\n')


file.close()

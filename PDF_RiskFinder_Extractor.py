
#!pip install PyPDF2
#!pip install nltk

#need this unzip command if using Kaggle
#!unzip /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora/

import PyPDF2
import re
import csv
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer

pdf_path = '/kaggle/input/imperial-annual-report-202324/Annual Report 2023 24.pdf'

#open in read binary mode
file = open(pdf_path,'rb')

reader = PyPDF2.PdfReader(file)

num_pages = len(reader.pages)

print(f'The pdf contains {num_pages} pages')

# Create a list of words associated with "risk" using WordNet
risk_synonyms = set()
for syn in wordnet.synsets('risk'):
    for lemma in syn.lemmas():
        risk_synonyms.add(lemma.name())

risk_synonyms = list(risk_synonyms)
#print(f'Words associated with "risk": {risk_synonyms}')

# Initialize the PorterStemmer
stemmer = PorterStemmer()

# Stem the risk-related terms
stemmed_risk_terms = [stemmer.stem(term) for term in risk_synonyms]

# Function to extract paragraphs containing risk-related terms
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

# Print the risk-related paragraphs with page numbers
for i, (paragraph, page_num) in enumerate(all_risk_paragraphs):
    print(f'Paragraph {i+1} (Page {page_num}‡):')
    print(paragraph)
    print('\n')

file.close()

"""
File: PDF_Key_Dates_Extractor.py
Author: EC
Created: 2024-08-21

Description: 
The script scans and extracts the dates from a PDF file, recording the associated page number of where the date was found.
Script can help identify key dates from Board and Annual Performance reports.

Sample report, Annual Report 2023 24
https://www.imperial.nhs.uk/about-us/how-we-are-doing/annual-reports

"""

import PyPDF2
import re
import csv

def extract_dates_with_page_numbers(pdf_path):
    # open PDF in read binary mode
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        # Empty list to store dates and associated page numbers.
        found_dates = []
        
        # Loop through each page extracting text from each page.
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Exclude the footer from date search
            footer_pattern = re.compile(r'Annual Report 2023/24')
            text = re.sub(footer_pattern, '', text)
            
            # Find dates in the text using regular expression. Either a full date e.g. 1 September 2024 or just the year between 2023 to 2030
            dates = re.findall(r'\b(?:\d{1,2} )?\w+ \d{4}\b', text)
            years = re.findall(r'\b(202[3-9]|2030)\b', text)
            
            # append found full dates
            for date in dates:
                found_dates.append((date, page_num + 1))  # Page numbers are 1-based
                
            # append found years only
            for year in years:
                found_dates.append((year, page_num + 1))  # Page numbers are 1-based
    
    return found_dates

pdf_path = '/kaggle/input/imperial-annual-report-202324/Annual Report 2023 24.pdf'
# call fucntion 
found_dates = extract_dates_with_page_numbers(pdf_path)
output_csv = 'found_dates.csv'

# Write the found dates to a CSV file
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Page Number'])
    for date, page_num in found_dates:
        writer.writerow([f"{date} (page {page_num})"])

print(f"Results written to {output_csv}")

"""
File: ReadFlatFileInBatches.py
Author: EC
Created: 2024-02-26

"""

import pandas as pd
import time

#Location of flat file to process
file_path = r'D:\NationalData\Load\tags.txt'

#start timer
start_time = time.time()

#read the file, file has no header
try:
    #Batch the data into chunks of 100,000 rows at a time
    chunk_size = 100000
    
    df_chunks = pd.read_csv(file_path, sep= '|', engine = 'python', encoding ='unicode_escape', header= None, chunksize = chunk_size)
    
    #Empty data frame to store chunks
    df = pd.DataFrame()
    
    #Process each data chunk and concatenate
    for chunk in df_chunks:
        df = pd.concat([df, chunk], ignore_index= True)
        
        print(f"Number of rows in the text file: {len(df):,}")
        
        #Calculate the execution time
        end_time = time.time()
        execution_time = end_time - start_time
        formattted_execution_time = f"{execution_time:.4f}"
        
        print(f"Execution time: {formattted_execution_time} seconds")
        
except FileNotFoundError:
    print(f"file  '{file_path}' not found")




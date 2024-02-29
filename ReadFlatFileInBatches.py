"""
File: ReadFlatFileInBatches.py
Author: EC
Created: 2024-02-26

Description: 
    Reads a flat file in chunks, concatenates the chunks, and handles errors.

"""

import pandas as pd
import time
import os

# Batch the data into chunks of 100,000 rows at a time
def chunkfile(file_path: str, chunk_size: int = 100000):

    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        # Start timer
        start_time = time.time()

        # Read the file, file has no header
        df_chunks = pd.read_csv(file_path, sep='|', engine='python', encoding='unicode_escape', header=None, chunksize=chunk_size)

        # Empty data frame to store chunks
        df = pd.DataFrame()

        # Process each data chunk and concatenate
        for chunk in df_chunks:
            df = pd.concat([df, chunk], ignore_index=True)

        print(f"Number of rows in the text file: {len(df):,}")

        # Calculate the execution time
        end_time = time.time()
        execution_time = end_time - start_time
        formatted_execution_time = f"{execution_time:.4f}"
        print(f"Execution time: {formatted_execution_time} seconds")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def main():
    input_file_path = r'D:\NationalData\Load\tags.txt'
    chunkfile(input_file_path)

main()




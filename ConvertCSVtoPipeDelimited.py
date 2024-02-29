"""
File: ReadFlatFileInBatches.py
Author: EC
Created: 2024-02-26

Description: 
Script converts a CSV to a text file which is pipe delimited. The original CSV is then moved to the Processed folder 

"""
import os
import pandas as pd

def process_csv(input_folder: str, output_folder: str):
    try:
        # The input and output paths
        input_csv_path = os.path.join(input_folder, 'population.csv')
        output_txt_path = os.path.join(output_folder, 'population.txt')

        # Read the source CSV file
        df = pd.read_csv(input_csv_path, sep=',')

        # Output as a text file which is pipe delimited
        df.to_csv(output_txt_path, sep='|', index=False)

        # Create a processed folder if not present
        processed_folder = os.path.join(output_folder, 'processed')
        os.makedirs(processed_folder, exist_ok=True)

        # Move the original CSV to the processed folder
        original_csv_filename = os.path.basename(input_csv_path)
        new_csv_path = os.path.join(processed_folder, original_csv_filename)
        os.rename(input_csv_path, new_csv_path)

        print(f"CSV file moved to {new_csv_path}")

    except FileNotFoundError:
        print(f"File not found: '{input_csv_path}' not found, please check the file path")

# List the file paths to use
def main():
    input_folder_path = r'D:\NationalData\Load\ImportData\Input'
    output_folder_path = r'D:\NationalData\Load\Output'
    process_csv(input_folder_path, output_folder_path)


if __name__ == "__main__":
    main()
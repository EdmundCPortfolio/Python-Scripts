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
        # Check if input folder exists
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")

        # Check if output folder exists or create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created output folder: {output_folder}")

        # Input and output paths
        input_csv_path = os.path.join(input_folder, 'population.csv')
        output_txt_path = os.path.join(output_folder, 'population.txt')

        # Read in orginal CSV file
        df = pd.read_csv(input_csv_path, sep=',')

        # Output text file with pipe delimiter
        df.to_csv(output_txt_path, sep='|', index=False)

        # Create the Processed folder if it doesn't exist
        processed_folder = os.path.join(output_folder, 'processed')
        os.makedirs(processed_folder, exist_ok=True)

        # Move the original CSV file to the Processed folder
        original_csv_filename = os.path.basename(input_csv_path)
        new_csv_path = os.path.join(processed_folder, original_csv_filename)
        os.rename(input_csv_path, new_csv_path)

        print(f"CSV file moved to {new_csv_path}")
        print(f'Text file exported to {output_txt_path}')

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")


def main():
    input_folder_path = r'D:\NationalData\Load\ImportData\Input'
    output_folder_path = r'D:\NationalData\Load\Output'
    process_csv(input_folder_path, output_folder_path)

if __name__ == "__main__":
    main()

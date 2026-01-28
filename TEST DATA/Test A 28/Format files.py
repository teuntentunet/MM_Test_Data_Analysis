#Import packages so that I can manipulate the files in the folder
import os
import numpy as np
import pandas as pd

#Rename all files in the folder that are structured like MM-TestA-28012026-1.25 NULL.csv to MM-TestA 28-1.25 NULL.csv
def rename_files_in_folder(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.startswith("MM-Test") and filename.endswith(".csv"):
            parts = filename.split("-")
            if len(parts) >= 3:
                test_part = parts[1]
                date_part = parts[2]
                rest_of_filename = "-".join(parts[3:])
                
                #Extract test letter and number
                test_letter = ''.join(filter(str.isalpha, test_part))
                test_number = ''.join(filter(str.isdigit, date_part))[:2] #

                #strip the spaces in rest of filename
                new_rest_of_filename = rest_of_filename.strip()
                
                new_test_part = f"{test_letter} {test_number}"
                new_filename = f"MM-{new_test_part}-{new_rest_of_filename}"
                
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} to {new_filename}")

if __name__ == "__main__":
    #set path to be current folder
    folder_path = 'Test DATA/Test A 28'
    rename_files_in_folder(folder_path)


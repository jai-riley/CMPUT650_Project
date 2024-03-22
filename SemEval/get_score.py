import csv

csv_file_path = 'SemEval2024-Task1/labels/arb_test_with_labels.csv'
target_column = 'Score'

import numpy as np

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
# Open the csv file

def get_values(csv_file_path, target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        # Create a csv reader
        csvreader = csv.DictReader(csvfile)

        # Check if the target column is present in the header
        if target_column not in csvreader.fieldnames:
            print(f"Error: Column '{target_column}' not found in the csv file.")
        else:
            # Extract values from the target column
            column_values = [0 for row in range(250)]
            #print(len(column_values))
            for row in csvreader:
                #print(row["PairID"][-4:])
                #column_values[int(row["PairID"][-4:])] = float(row[target_column])
                column_values = [float(row[target_column]) for row in csvreader ]

            # Print the extracted values
            #print(f"All values in the '{target_column}' column: { column_values}")
            return column_values



#print(get_values(csv_file_path,target_column))

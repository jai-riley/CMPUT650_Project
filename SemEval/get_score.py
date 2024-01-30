import csv

csv_file_path = 'out_1.csv'
target_column = 'Pred_Score'

# Open the csv file
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a csv reader
    csvreader = csv.DictReader(csvfile)

    # Check if the target column is present in the header
    if target_column not in csvreader.fieldnames:
        print(f"Error: Column '{target_column}' not found in the csv file.")
    else:
        # Extract values from the target column
        column_values = [float(row[target_column]) for row in csvreader]

        # Print the extracted values
        print(f"All values in the '{target_column}' column: {column_values}")

import csv

tsv_file_path = 'out_train.tsv'
target_column = 'Score'

# Open the TSV file
with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsvfile:
    # Create a TSV reader
    tsvreader = csv.DictReader(tsvfile, delimiter='\t')

    # Check if the target column is present in the header
    if target_column not in tsvreader.fieldnames:
        print(f"Error: Column '{target_column}' not found in the TSV file.")
    else:
        # Extract values from the target column
        column_values = [float(row[target_column]) for row in tsvreader]

        # Print the extracted values
        print(f"All values in the '{target_column}' column: {column_values}")

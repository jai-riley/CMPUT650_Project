import csv
import random

# Function to read data from TSV file
def read_tsv_file(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

# Function to randomly select half of the indices
def randomly_select_half(data):
    num_indices = len(data)
    half_indices = random.sample(range(num_indices), k=num_indices // 2)
    selected_data = [data[i] for i in half_indices]
    unselected_data = [data[i] for i in range(num_indices) if i not in half_indices]
    return selected_data, unselected_data

# Function to write data to TSV file
def write_tsv_file(file_path, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=data[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(data)

# Path to the input TSV file
input_tsv_file_path = 'eng_dev_trackD.tsv'

# Read data from the input TSV file
data_from_tsv = read_tsv_file(input_tsv_file_path)

# Randomly select half of the indices
spanish_english, english_spanish = randomly_select_half(data_from_tsv)
print(spanish_english)
for x in spanish_english:
    del x["Text1"]
    del x["Text2 Translation"]

for x in english_spanish:
    del x["Text2"]
    del x["Text1 Translation"]

#write_tsv_file('output.tsv',spanish_english)
write_tsv_file('output1.tsv',english_spanish)

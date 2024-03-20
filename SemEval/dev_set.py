import csv
import random
import os
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

def select_every_other(data):
    num_indices = len(data)
    one = []
    for x in range(num_indices):
        if x % 2 == 0:
            one.append(x)
    selected_data = [data[i] for i in one]
    unselected_data = [data[i] for i in range(num_indices) if i not in one]
    return selected_data, unselected_data

# Function to write data to TSV file
def write_tsv_file(file_path, data):
    with open(file_path, 'a', newline='', encoding='utf-8') as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=['PairID', 'Text1', 'Text2'])
        if os.path.getsize(file_path) == 0:
            writer.writeheader()
        print(data)
        writer.writerows(data)

# Path to the input TSV file
input_tsv_file_path = 'eng_dev_trackD.tsv'

# Read data from the input TSV file
data_from_tsv = read_tsv_file(input_tsv_file_path)

# Randomly select half of the indices
spanish_english, english_spanish = select_every_other(data_from_tsv)
#print(spanish_english)
for x in spanish_english:
    del x["Text1"]
    del x["Text2 Translation"]
    x["Text1"] = x["Text1 Translation"]
    del x["Text1 Translation"]

for x in english_spanish:
    del x["Text2"]
    del x["Text1 Translation"]
    x["Text2"] = x["Text2 Translation"]
    del x["Text2 Translation"]

write_tsv_file('eng_span_trackD.csv',spanish_english)
write_tsv_file('eng_span_trackD.csv',english_spanish)

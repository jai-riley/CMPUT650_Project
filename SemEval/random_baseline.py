import csv
import os
from random import randint

def get_column(csv_file_path, target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        if target_column not in csvreader.fieldnames:
            print(f"Error: Column '{target_column}' not found in the csv file.")
        else:
            return [row[target_column] for row in csvreader]


all_files = os.listdir("SemEval2024-Task1/labels")


print(all_files)

for file in all_files:
    with open(f"random_baseline/{file}", 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["PairID","Pred_Score"])
        ids = get_column(f"SemEval2024-Task1/labels/{file}", "PairID")
        for pair in ids:
            num = randint(0, 101)
            csvwriter.writerow([pair,num/100])

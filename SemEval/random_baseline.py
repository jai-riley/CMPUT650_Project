import csv
import os
from random import randint
from evaluate import eval,avg
def get_column(csv_file_path, target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        if target_column not in csvreader.fieldnames:
            print(f"Error: Column '{target_column}' not found in the csv file.")
        else:
            return [row[target_column] for row in csvreader]


def get_values(path):
    all_files = os.listdir(path)
    for file in all_files:
        with open(f"random_baseline/{file}", 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["PairID","Pred_Score"])
            ids = get_column(f"{path}/{file}", "PairID")
            for pair in ids:
                num = randint(0, 101)
                csvwriter.writerow([pair,num/100])



def main():
    for x in range(3000):
        print(x)
        get_values("SemEval2024-Task1/labels")
        eval()
    avg()


if __name__ == "__main__":
    main()

import csv
import pandas as pd
import math

data = []

with open("s15_a2_sentences.txt", 'r', encoding='utf-8-sig') as file:
    lines = file.readlines()
    for line in lines:
        sentence = line.split('\t')
        data.append([sentence[0].strip(), sentence[1].strip(), sentence[2].strip()])

with open('s15_a2_sentences.tsv', 'w', newline='', encoding='utf-8-sig') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    writer.writerows(data)

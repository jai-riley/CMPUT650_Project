import pandas as pd
import translators as ts


def get_nth_line(file_path, n):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if 1 <= n <= len(lines):
            return lines[n - 1]


def get_alignment(token_number, sentence_number):
    synset_line = get_nth_line('../Data/synset.txt', sentence_number + 1)
    synset_line = synset_line.strip()
    synsets = synset_line.split(" ")
    alignments = ""
    for synset in synsets:
        if int(synset.split("-")[0]) == token_number:
            if int(synset.split("-")[1]) < len(target_sentences[sentence_number].split(" ")):
                alignments += (target_sentences[sentence_number].split(" ")[int(synset.split("-")[1])] + " ")
    return alignments.strip()


df = pd.read_csv('../Data/process_s15.tsv', sep='\t', header=None, encoding="utf-8-sig")

source_sentences = []
target_sentences = []

temp = "s001"
sentence = ""
for index, row in enumerate(df.values):
    if row[0].split(".")[1] != temp:
        source_sentences.append(sentence.strip())
        sentence = ""
    sentence += row[1] + " "
    temp = row[0].split(".")[1]
source_sentences.append(sentence.strip())

for s in source_sentences:
    result = ts.translate_text(translator='google', query_text=s, from_language='en', to_language='fa')
    target_sentences.append(result)
    print(result)

new_column = []

temp = "s001"
sentence_number = 0
for index, row in enumerate(df.values):
    if row[0].split(".")[1] != temp:
        sentence_number += 1
    temp = row[0].split(".")[1]
    token_number = int(row[0].split(".")[2][1:]) - 1
    alignment = get_alignment(token_number, sentence_number)
    if alignment == "":
        new_column.append("n/a")
    else:
        new_column.append(alignment)

df = pd.read_csv("../Data/process_s15.tsv", sep='\t', encoding="utf-8-sig", header=None)
df[len(df.columns)] = new_column
df.to_csv("../Data/new_process_s15.tsv", index=False, header=False, encoding="utf-8-sig")

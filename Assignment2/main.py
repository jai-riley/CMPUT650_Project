import pandas as pd
import translators as ts
from hazm import *
import csv
import math
from amuse_request import send_request

# This function calls `the'send_request` function from the `amuse_requst` calss and returns the response
def get_persian_bable(num_line, persian_index):
    token = get_persian_token(num_line - 1, persian_index)
    sentence = target_sentences[num_line - 1]
    response = send_request(sentence)
    if token == "":
        return ""
    else:
        return response[persian_index]["bnSynsetId"]

# This function returns the nth Farsi's token for a sentence
def get_persian_token(num_line, persian_index):
    if persian_index < len(word_tokenize(target_sentences[num_line])):
        return word_tokenize(target_sentences[num_line])[persian_index]
    else:
        return ""

# This function returns the nth line of a file
def get_nth_line(file_path, n):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if 1 <= n <= len(lines):
            return lines[n - 1]

# This function returns the Farsi-aligned token index with the English token
def get_synset(num_line, english_index):
    synset_line = get_nth_line('synset.txt', num_line)
    synsets = synset_line.split(" ")
    str = ""
    for synset in synsets:
        if int(synset.split("-")[0]) == english_index:
            str += get_persian_token(num_line - 1, int(synset.split("-")[1])) + " "

    if str != "" and str != " ":
        persian_sentence = target_sentences[num_line - 1]
        pos = [item[1] for item in tagger.tag(word_tokenize(persian_sentence)) if str.strip().split(" ")[0] in item]

        return str.strip(), pos[0]
    else:
        return str.strip(), []

# This function returns all the Farsi tokens aligned with English tokens
def get_persian_token_id(num_line, english_index):
    synset_line = get_nth_line('synset.txt', num_line)
    synsets = synset_line.split(" ")
    str = ""
    for synset in synsets:
        if int(synset.split("-")[0]) == english_index:
            str += synset.split("-")[1] + " "
    return str.strip()

# This function returns the number of Farsi tokens without any sense tags and the number of all tokens
def count_without_tag():
    without_sense = 0
    num_token = 0
    for sentence in target_sentences:
        response = send_request(sentence)
        num_token += len(response)
        for res in response:
            if res["bnSynsetId"] == "O":
                without_sense += 1

    print("without_sense" + str(without_sense))
    print("\n")
    print("num_token" + str(num_token))


df = pd.read_csv('process_s15.tsv', sep='\t', header=None)

source_sentences = []
source_dict_list = []
target_sentences = []
target_dict_list = []

temp = "s001"
sentence = ""
dict = {}
for index, row in enumerate(df.values):
    if row[0].split(".")[1] != temp:
        source_sentences.append(sentence)
        source_dict_list.append(dict)
        sentence = ""
        dict = {}
    sentence += row[1] + " "
    temp = row[0].split(".")[1]
    dict[index] = row[4]
source_sentences.append(sentence)
source_dict_list.append(dict)

for s in source_sentences:
    result = ts.translate_text(translator='google', query_text=s, from_language='en', to_language='fa')
    target_sentences.append(result)
    print(result)

lemmatizer = Lemmatizer()
tagger = POSTagger(model='pos_tagger.model')

count_without_tag()
input()

data = []

df = pd.read_csv('process_s15.tsv', sep='\t', header=None)

for row in df.values:
    id = row[0].split(".")
    doc_id = int(id[0][1:])
    sentence_id = int(id[1][1:])
    token_id = int(id[2][1:])

    if doc_id == 2:
        sentence_id += 38
    if doc_id == 3:
        sentence_id += (38 + 54 - 1)
    if doc_id == 4:
        sentence_id += (38 + 54 + 22)

    persian_token = get_persian_token_id(sentence_id, token_id - 1)
    synset, pos = get_synset(sentence_id, token_id - 1)

    if len(persian_token.split(" ")[0]) > 0:
        persian_token = int(persian_token.split(" ")[0])
        bable_id = get_persian_bable(sentence_id, persian_token)
    else:
        bable_id = float("nan")

    if synset == "":
        synset = float("nan")

    if type(row[4]) == str and bable_id == "O":
        bable_id = float("nan")
    elif type(row[4]) != str and bable_id == "O":
        bable_id = float("nan")
    data.append([row[0], row[1], row[2], row[3], row[4], synset, bable_id])

count = 0
for d in data:
    if d[4] == d[6]:
        count += 1
print("The number of matched sense tags : " + str(count))

with open('s15_a2_tokens.tsv', 'w', newline='', encoding='utf-8-sig') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    writer.writerows(data)

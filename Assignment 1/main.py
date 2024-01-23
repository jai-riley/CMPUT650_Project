import pandas as pd
import translators as ts
from hazm import *
import csv

def get_nth_line(file_path, n):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if 1 <= n <= len(lines):
            return lines[n - 1]

def get_synset(num_line, persian_index):
    synset_line = get_nth_line('synset.txt', num_line + 1)
    synsets = synset_line.split(" ")
    for synset in synsets:
        if int(synset.split("-")[1]) == persian_index:
            if int(synset.split("-")[0]) < len(list(source_dict_list[num_line].values())):
                return list(source_dict_list[num_line].values())[int(synset.split("-")[0])]
            else:
                return "nan"

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
print(source_dict_list)
for s in source_sentences:
    result = ts.translate_text(translator='google', query_text=s, from_language='en', to_language='fa')
    target_sentences.append(result)
    print(result)

print(target_sentences)

print(word_tokenize(target_sentences[0]))
lemmatizer = Lemmatizer()
tagger = POSTagger(model='pos_tagger.model')
data = []
for sentence_index, s in enumerate(target_sentences):
    for token_index, token in enumerate(word_tokenize(s)):
        doc_id = ""
        sentence_id = ""
        token_id = ""
        if sentence_index + 1 <= 38:
            doc_id = str(1).zfill(3)
            sentence_id = str(sentence_index + 1).zfill(3)
            token_id = str(token_index + 1).zfill(3)
        elif sentence_index + 1 > 38 and sentence_index + 1 <= 92:
            doc_id = str(2).zfill(3)
            sentence_id = str(sentence_index + 1 - 38).zfill(3)
            token_id = str(token_index + 1).zfill(3)
        elif sentence_index + 1 > 92 and sentence_index + 1 <= 114:
            doc_id = str(3).zfill(3)
            sentence_id = str(sentence_index + 1 - 92).zfill(3)
            token_id = str(token_index + 1).zfill(3)
        else:
            doc_id = str(4).zfill(3)
            sentence_id = str(sentence_index + 1 - 114).zfill(3)
            token_id = str(token_index + 1).zfill(3)
        id = "d" + doc_id + "." + "s" + sentence_id + "." + "t" + token_id
        pos = [item[1] for item in tagger.tag(word_tokenize(s)) if token in item]
        synset = get_synset(sentence_index, token_index)
        data.append((id, token, lemmatizer.lemmatize(token), pos[0], synset))

df = pd.DataFrame(data, columns=['id', 'token', 'lemmatize', 'pos', 'sense'])
csv_file_path = 'processed_fa.csv'
df.to_csv(csv_file_path, header=False, index=False, encoding='utf-8-sig')

# with open('input.txt', 'a', encoding="utf-8") as f:
#     for index, s in enumerate(source_sentences):
#         f.write(s + " ||| " + target_sentences[index] + "\n")

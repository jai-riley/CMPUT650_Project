import pandas as pd
import translators as ts


def get_nth_line(n):
    with open('../Data/synset.txt', 'r') as file:
        lines = file.readlines()
        if 1 <= n <= len(lines):
            return lines[n - 1].strip()


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

with open('../Data/new_processed_s15.txt', 'a', encoding="utf-8") as f:
    for index, s in enumerate(source_sentences):
        f.write(s + "\t" + target_sentences[index] + "\t" + get_nth_line(index + 1) + "\n")

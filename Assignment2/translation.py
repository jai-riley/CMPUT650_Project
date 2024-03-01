from datasets import load_dataset
from nltk.translate import meteor
from nltk import word_tokenize
import nltk

dataset = load_dataset("persiannlp/parsinlu_translation_en_fa")

# print(dataset['test'][0])

print(set(dataset['test']['category']))

for i in dataset['test']:
    print(i['source'])
    print(i['targets'])
    input()

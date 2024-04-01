import requests
import csv
import os
from similarity import get_score
from nltk.corpus import wordnet




def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def union(lst1, lst2):
    lst3 = [x for x in lst1]
    for x in lst2:
        if x not in lst3:
            lst3.append(x)
    return lst3


"""def get_score(lst1, lst2):
    lst3 = intersection(lst1, lst2)
    if len(union(lst1, lst2)) == 0:
        return 0
    else:
        return len(lst3) / len(union(lst1, lst2))
"""

def read_csv_file(file_path):
    data = []
    count = 0
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r = []
            # print(row['PairID'])
            text = row['Text'].split('\n')
            r.append({'text': text[0].lower(), 'lang': "EN"})
            r.append({'text': text[1].lower(), 'lang': "EN"})

            #r.append({'text': row['Text1 Translation'].lower(), 'lang': "EN"})
            #r.append({'text': row['Text2 Translation'].lower(), 'lang': "EN"})
            score = get_wsd(r)
            x = {'PairID': row['PairID'], "Pred_Score": f'{score:.2f}'}
            lst.append(x)
            count +=1
            print(f"Done row {count}")

    return data


def get_wsd(data):
    try:
        response = requests.post(api_url, headers=headers, json=data)
        concepts = []
        if response.status_code == 200:
            json_response = response.json()
            for sentence in json_response:
                l = []
                #print(sentence)
                for token in sentence['tokens']:
                    # note here that the original data was from bnSynsetId
                    if len(token['nltkSynset']) != 1:
                        l.append(token['nltkSynset'])
                        # print(token['text'])
                concepts.append(l)
            # print(get_score(concepts[0], concepts[1]))
            return get_score(concepts[0], concepts[1],0.8)

        else:
            print(f"Error: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")


def write_csv_file(file_path, data):
    # print(data[0].keys())
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


api_url = "http://127.0.0.1:12346/api/model"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

"""lst = []
csv_file_path = 'eng_train.csv'
output_file = "eng_train.csv"
data_from_csv = read_csv_file(csv_file_path)
write_csv_file(output_file, lst)
"""

all_dirs = os.listdir("SemEval2024-Task1")
all_files = ["afr2eng_dev.csv",
     "afr2eng_test.csv",
     "amh2eng_dev.csv",
     "amh2eng_test.csv",
     "arb2eng_dev.csv",
     "arb2eng_test.csv",
     "arq2eng_dev.csv",
     "arq2eng_test.csv",
     "ary2eng_dev.csv",
     "ary2eng_test.csv",
     "esp2eng_dev.csv",
     "esp2eng_test.csv",
     "hau2eng_dev.csv",
     "hau2eng_test.csv",
     "hin2eng_dev.csv",
     "hin2eng_test.csv",
     "ind2eng_dev.csv",
     "ind2eng_test.csv",
     "mar2eng_dev.csv",
     "mar2eng_test.csv",
     "tel2eng_dev.csv",
     "tel2eng_test.csv",
     "kin2eng_dev.csv",
"kin2eng_test.csv"]

completed_files = ["amh2eng_dev.csv,"
      "amh2eng_test.csv",
      "arb2eng_dev.csv",
      "arb2eng_test.csv",
      "arq2eng_dev.csv",
      "arq2eng_test.csv",
      "ary2eng_dev.csv",
      "ary2eng_test.csv",
      "eng_train.csv",
      "esp2eng_dev.csv",
      "esp2eng_test.csv",
      "hau2eng_dev.csv",
      "hau2eng_test.csv",
      "hin2eng_dev.csv",
      "hin2eng_test.csv",
      "ind2eng_dev.csv",
      "ind2eng_test.csv"]


dirs = []
for file in all_dirs:
    if file[-7:] == "dev.csv":
        dirs.append(file)
dirs.remove("eng_dev.csv")
print(dirs)
#dirs.remove("eng_test.csv")
#dirs.remove("esp_dev.csv")

count = 0
#dirs = [x for x in all_files if x not in completed_files]
dirs = ['eng_dev.csv']
#lang = "EN"


# rerun relatedness for hin
for file in dirs:
    lst = []
    print(f"Starting file: {file}")
    csv_file_path = "SemEval2024-Task1/" + file
    output_file = "SemEval2024-Task1/outputTHM/" + file
    data_from_csv = read_csv_file(csv_file_path)
    write_csv_file(output_file, lst)
    count += 1
    print(f"Finished {file}: {count}/{len(dirs)}")

"""[{'text': 'two championships, three all-star wins, seven straight feature wins.', 'lang': 'EN'}, {'text': '2 championship, 3 all-stars victory, 7 straight wins.', 'lang': 'EN'}]"""

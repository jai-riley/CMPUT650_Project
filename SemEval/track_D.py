import requests
import csv
import os
from nltk.corpus import wordnet
#from similarity import get_score


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def union(lst1, lst2):
    lst3 = [x for x in lst1]
    for x in lst2:
        if x not in lst3:
            lst3.append(x)
    return lst3


def get_score(lst1, lst2):
    lst3 = intersection(lst1, lst2)
    #return get_similarity(lst1,lst2) / len(union(lst1,lst2))
    if len(union(lst1,lst2)) == 0:
        return 0
    return len(lst3) / len(union(lst1,lst2))


"""def get_similarity(lst1, lst2):
    #inter = intersection(lst1, lst2)
    l1 = {}
    l2 = {}
    for item in set(lst1):
            l1[item] = 0
    for item in set(lst2):
            l2[item] = 0
    for item in l1.keys():
        for item2 in l2.keys():
            synl1 = wordnet.synset(item)
            synl2 = wordnet.synset(item2)
            val = synl1.wup_similarity(synl2)
            if val > l1[item] and val >= 0.3:
                l1[item] = val
    for item in l2.keys():
        for item2 in l1.keys():
            synl1 = wordnet.synset(item)
            synl2 = wordnet.synset(item2)
            val = synl1.wup_similarity(synl2)
            if val > l2[item] and val >= 0.3:
                l2[item] = val
    return sum(l1.values())+sum(l1.values())

"""

def read_csv_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r = []
            # print(row['PairID'])
            #text = row['Text'].split('\n')
            #r.append({'text': text[0].lower(), 'lang': lang})
            #r.append({'text': text[1].lower(), 'lang': lang})
            #t1 = text[0].lower()
            #t2 = text[1].lower()
            t1 = row['Text1'].lower()
            t2 = row['Text2'].lower()
            print(row["PairID"][-1])
            if int(row["PairID"][-1]) % 2 == 0:
                r.append({'text': t1, 'lang': "ES"})
                r.append({'text': t2, 'lang': "EN"})
            else:
                r.append({'text': t1, 'lang': "EN"})
                r.append({'text': t2, 'lang': "ES"})
            score = get_wsd(r)


            #r = []
            #r.append({'text':t1, 'lang': "EN"})
            #r.append({'text': t2, 'lang': "EN"})
            #score_3 = get_wsd(r)

            x = {'PairID': row['PairID'], "Pred_Score": f'{score:.2f}'}
            lst.append(x)
            #print(max(score_1,score_2,score_3))



def get_wsd(data):
    try:
        response = requests.post(api_url, headers=headers, json=data)
        concepts = []
        if response.status_code == 200:
            json_response = response.json()
            for sentence in json_response:
                l = []
                for token in sentence['tokens']:
                    if len(token['nltkSynset']) != 1:
                        l.append(token['nltkSynset'])
                        # print(token['text'])
                concepts.append(l)
            # print(get_score(concepts[0], concepts[1]))
            return get_score(concepts[0], concepts[1])

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
"""
lst = []
csv_file_path = 'eng_span_trackD.csv'
output_file = "eng_span_trackD_out.csv"
data_from_csv = read_csv_file(csv_file_path)
write_csv_file(output_file, lst)
"""

all_dirs = os.listdir("sts")

dirs = []
for file in all_dirs:
    if file != "output" and file[0:5] != "track" and file != "trans_eng_esp_dev.csv":
        dirs.append(file)
count = 0
#dirs = [x for x in l if x not in l2]
#dirs = ["eng_dev.csv"]
dirs = ["eng_esp_dev.csv"]

for file in dirs:
    lst = []
    print(f"Starting file: {file}")
    csv_file_path = "sts/" + file
    output_file = "SemEval2024-Task1/output/" + file
    data_from_csv = read_csv_file(csv_file_path)
    write_csv_file(output_file, lst)
    count += 1
    print(f"Finished {file}: {count}/{len(dirs)}")

"""for file in dirs:
    lst = []
    print(f"Starting file: {file}")
    csv_file_path = "sts/" + file
    output_file = "sts/output/" + file
    data_from_csv = read_csv_file(csv_file_path)
    write_csv_file(output_file, lst)
    count += 1
    print(f"Finished {file}: {count}/{len(dirs)}")
"""
"""[{'text': 'two championships, three all-star wins, seven straight feature wins.', 'lang': 'EN'}, {'text': '2 championship, 3 all-stars victory, 7 straight wins.', 'lang': 'EN'}]"""

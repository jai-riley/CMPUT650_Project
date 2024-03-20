import requests
import csv
import os
from nltk.corpus import wordnet

# https://babelnet.io/v6/getSynset?id={babel_id}&key={api_key}

lang = "AF"
lst = []


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def union(lst1, lst2):
    lst3 = [x for x in lst1]
    for x in lst2:
        if x not in lst3:
            lst3.append(x)
    return lst3


def get_score(lst1, lst2, thres=0):
    lst3 = intersection(lst1, lst2)
    # return get_similarity(lst1,lst2) / len(union(lst1,lst2))
    if thres == 0:
        if (len(lst1) + len(lst2)) == 0:
            return 0
        else:
            score = get_similarity(lst1, lst2) / (len(lst1) + len(lst2))

    else:
        if len(union(lst1, lst2)) == 0:
            return 0
        else:
            score = get_similarity(lst1, lst2, thres) / len(union(lst1, lst2))
    return min(1, score)
    # return score


def avg_path(dict, item, val):
    if val > dict[item]:
        dict[item] = val


def threshold_path(dict, item, val, thres):
    if val > thres:
        dict[item] = 1


def get_similarity(lst1, lst2, thres=0):
    # inter = intersection(lst1, lst2)
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
            try:
                val = synl1.wup_similarity(synl2)
            except:
                val = 0
            if thres == 0:
                avg_path(l1, item, val)
            else:
                threshold_path(l1, item, val, thres)
    for item in l2.keys():
        for item2 in l1.keys():
            synl1 = wordnet.synset(item)
            synl2 = wordnet.synset(item2)
            try:
                val = synl1.wup_similarity(synl2)
            except:
                val = 0

            if thres == 0:
                avg_path(l2, item, val)
            else:
                threshold_path(l2, item, val, thres)
    return sum(l1.values()) + sum(l1.values())


def read_csv_file(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['PairID'])
            r = []
            #text = row['Text'].split('\n')
            t1 = row['Text1 Translation'].lower()
            t2 = row['Text2 Translation'].lower()
            r.append({'text': t1, 'lang': "EN"})
            r.append({'text': t2, 'lang': "EN"})
            #r.append({'text': text[0].lower(), 'lang': "EN"})
            #r.append({'text': text[1].lower(), 'lang': "ES"})
            score = get_wsd(r)
            x = {'PairID': row['PairID'], "Pred_Score": f'{score:.2f}'}
            lst.append(x)

    return data


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
"""
csv_file_path = 'SemEval2024-Task1/afr2eng_test.csv'
output_file = "SemEval2024-Task1/outputTHM/afr2eng_test.csv"
data_from_csv = read_csv_file(csv_file_path)
write_csv_file(output_file, lst)
"""
"""[{'text': 'two championships, three all-star wins, seven straight feature wins.', 'lang': 'EN'}, {'text': '2 championship, 3 all-stars victory, 7 straight wins.', 'lang': 'EN'}]"""

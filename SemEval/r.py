import requests
import csv
import os

lang = "ES"
lst =[]

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
    return len(lst3) / len(union(lst1,lst2))


def read_csv_file(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r = []
            text = row['Text'].split('\n')
            r.append({'text': text[0].lower(), 'lang': lang})
            r.append({'text': text[1].lower(), 'lang': lang})
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
                #print(sentence)
                for token in sentence['tokens']:
                    if len(token['bnSynsetId']) != 1:
                        l.append(token['bnSynsetId'])
                        # print(token['text'])
                concepts.append(l)
            #print(get_score(concepts[0], concepts[1]))
            return get_score(concepts[0], concepts[1])

        else:
            print(f"Error: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")


def write_csv_file(file_path, data):
    #print(data[0].keys())
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


api_url = "http://nlp.uniroma1.it/amuse-wsd/api/model"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}
csv_file_path = 'eng_train.csv'
output_file = "out_train.tsv"
data_from_csv = read_csv_file(csv_file_path)
write_csv_file(output_file,lst)

"""[{'text': 'two championships, three all-star wins, seven straight feature wins.', 'lang': 'EN'}, {'text': '2 championship, 3 all-stars victory, 7 straight wins.', 'lang': 'EN'}]"""

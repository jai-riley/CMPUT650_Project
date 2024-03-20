# take in sentences from a tsv file
# output .tsv file where the tokens from the senteces are
# each on their own line with sense tags if applciable
# also need the POS and lemmas

import requests
import csv

def read_csv_file(filename):
    sentences = {}
    current_sentence = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        id = ""
        for row in reader:
            if row.get("Token ID")[0:9] != id:
                if current_sentence:
                    sentences[id] = ' '.join(current_sentence)
                current_sentence = []
                id = row.get("Token ID")[0:9]
            token = row.get('Token')
            if token is not None:
                current_sentence.append(token)
        if current_sentence:
            sentences[id] = ' '.join(current_sentence)
    return sentences

def get_wsd(sentence,lang):
    try:
        response = requests.post(api_url, headers=headers, json=[{'text': sentence.lower(), 'lang':lang}])
        if response.status_code == 200:
            json_response = response.json()
            for sentence in json_response:
                return sentence
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

def write_to_csv(id, sentence, output_filename):
    with open(output_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        count = 1
        for token in sentence['tokens']:
            if count % 10 == count:
                tokenID = f't00{count}'
            elif count % 100 == count:
                tokenID = f't0{count}'
            else:
                tokenID = f't{count}'
            count += 1
            writer.writerow([f"{id}.{tokenID}",token['text'],token['lemma'],token['pos'],token['bnSynsetId']])


def main():
    try:
        sentences = read_csv_file(filename)
        print("\nSentences formed from tokens in the file:")
        for idx, sentence in sentences.items():
            wsd = get_wsd(sentence,"EN")
            write_to_csv(idx, wsd, output_file)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


filename = 'a3_tokens-English.csv'
output_file = "out_tokens.csv"

# this is the url for the offline version of AMuSE-WSD
api_url = "http://127.0.0.1:12346/api/model"

# Below is the url for the online version of AMuSE-WSD
# api_url = http://nlp.uniroma1.it/amuse-wsd/api/model

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


if __name__ == "__main__":
    main()

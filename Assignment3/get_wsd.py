"""
Jai Riley -> jrbuhr
Mohammad Tavakoli -> tavakol5
"""

import requests
import csv

def read_csv_file(filename):
    """
    Reads data from a CSV file and constructs sentences based on the tokens in the file.
    Args:
    - filename (str): The path to the CSV file to be read.
    Returns:
    - dict: A dictionary where keys are sentence IDs and values are sentences constructed from tokens.
    """
    # Dictionary to store sentences
    sentences = {}
    # List to hold tokens of the current sentence being constructed
    current_sentence = []

    # Open the CSV file for reading
    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        # Variable to track the current sentence ID
        id = ""
        # Iterate over each row in the CSV file
        for row in reader:
            # Extract the first 9 characters of the Token ID
            print(row)
            token_id_prefix = row.get('Token ID')[0:7]

            # If the current Token ID prefix is different from the previous one,
            # it means we are starting a new sentence
            if token_id_prefix != id:
                # If there are tokens in the current sentence, join them to form a sentence
                if current_sentence:
                    sentences[id] = ' '.join(current_sentence)
                # Reset the current sentence
                current_sentence = []
                # Update the current sentence ID
                id = token_id_prefix

            # Extract the token from the row
            token = row.get('Token')
            print(token)
            # If the token is not None, append it to the current sentence
            if token is not None:
                current_sentence.append(token)

        # After reading all rows, if there are tokens in the current sentence, join them to form a sentence
        if current_sentence:
            sentences[id] = ' '.join(current_sentence)
    # Return the constructed sentences
    return sentences

def get_wsd(sentence,lang):
    """
    Performs Word Sense Disambiguation (WSD) on a given sentence using a specified language.
    Args:
    - sentence (str): The input sentence for which WSD is to be performed.
    - lang (str): The language code indicating the language of the input sentence.
    Returns:
    - dict: A dictionary containing the WSD result for the input sentence.
    """
    data = [{'text':sentence.lower(), 'lang': lang}]
    try:
        # Send a POST request to the WSD API
        response = requests.post(api_url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()
            # Extract the WSD result for the sentence
            for sentence_wsd in json_response:
                #print(sentence_wsd)
                return sentence_wsd
        else:
            # Print error message if request was not successful
            print(f"Error: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        # Print error message if there was a request exception
        print(f"Request Exception: {e}")



def write_to_csv(id, sentence, output_filename):
    """
    Writes tokenized sentence data to a CSV file.
    Args:
    - id (str): The identifier for the sentence.
    - sentence (dict): A dictionary containing information about the sentence, including tokens.
    - output_filename (str): The path to the CSV file where the data will be written.
    Note:
    This function assumes that the 'sentence' parameter is in a specific format - the output of AMuSE-WSD
    """
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
            if token['bnSynsetId'] == 'O':
                sense = 'n/a'
            else:
                sense = token['bnSynsetId']
            writer.writerow([f"{id}.{tokenID}",token['text'],token['lemma'],token['pos'],sense])


def main():
    try:
        print("Getting sentences....")
        sentences = read_csv_file(filename)
        print(len(sentences))
        count = 1
        total = len(sentences.items())
        for idx, sentence in sentences.items():
            print(f"Sentence {count} of {total}....")
            wsd = get_wsd(sentence,lang)
            write_to_csv(idx, wsd, output_file)
            count += 1
        print("Done")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

lang = "FA"
filename = 'out_senses.csv'
output_file = "out_senses_farsi_GOLD.csv"

# this is the url for the offline version of AMuSE-WSD
api_url = "http://127.0.0.1:12346/api/model"

# Below is the url for the online version of AMuSE-WSD
# api_url = http://nlp.uniroma1.it/amuse-wsd/api/model

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


"""if __name__ == "__main__":
    main()
"""

import csv
from get_wsd import get_wsd

def find_multi_lexical_in_alignment(document_number: int, sentence_number: int, token: str) -> bool:
    for value in multi_lexical:
        document_id = int(value[0].split('.')[0][1:])
        sentence_id = int(value[0].split('.')[1][1:])
        if document_id == document_number and sentence_number == sentence_id and token == value[2]:
            return True

    return False


def get_sentence(document_number: int, sentence_number: int, first_token_id: str):
    with open("/Users/jairiley/Desktop/CMPUT650_Project/Assignment3/a3_tokens-WSDFarsi.csv", 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        next(reader)

        sentence = ""
        combined_word = ""
        for row in reader:
            document_id = int(row[0].split('.')[0][1:])
            sentence_id = int(row[0].split('.')[1][1:])
            if document_id == document_number and sentence_number == sentence_id:
                if first_token_id == row[0]:
                    next_row = next(reader)[1]
                    combined_word = row[1] + "\u200c" + next_row
                    sentence += row[1] + "\u200c" + next_row + " "
                else:
                    sentence += row[1] + " "

        return sentence, combined_word


multi_lexical = []

with open("/Users/jairiley/Desktop/CMPUT650_Project/Assignment3/a3_tokens-Aligned_Farsi_.csv", 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    next(reader)
    next(reader)

    for row in reader:
        if len(row[6].split('➕')) == 2:
            first_token_id = row[6].split('➕')[0]
            second_token_id = row[6].split('➕')[1]
            first_token = row[7].split('➕')[0]
            second_token = row[7].split('➕')[1]

            if int(second_token_id.split(".")[2][1:]) == int(first_token_id.split(".")[2][1:]) + 1:
                multi_lexical.append([first_token_id, second_token_id, first_token, second_token])

key_file = []
with open("/Users/jairiley/Desktop/CMPUT650_Project/Assignment3/a3_tokens-WSDFarsi.csv", 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    next(reader)

    for row in reader:
        if row[4] != 'n/a':
            key_file.append([row[0], row[0], row[4], ""])
            document_number = int(row[0].split('.')[0][1:])
            sentence_number = int(row[0].split('.')[1][1:])
            token_number = int(row[0].split('.')[2][1:])
            if find_multi_lexical_in_alignment(document_number=document_number, sentence_number=sentence_number,
                                               token=row[1]):
                next_token = row[0].split('.')[0] + "." + row[0].split('.')[1] + "." + "t" + str(
                    token_number + 1).zfill(3)
                sentence, combined_word = get_sentence(document_number=document_number, sentence_number=sentence_number,
                                                       first_token_id=row[0])
                wsd = get_wsd(sentence,"FA")["tokens"]
                for token in wsd:
                    if token["text"] == combined_word:
                        # retrieve the wn
                        key_file.append([row[0], next_token, token["bnSynsetId"], ""])

with open('/Users/jairiley/Desktop/CMPUT650_Project/Assignment3/key.csv', mode='w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(key_file)

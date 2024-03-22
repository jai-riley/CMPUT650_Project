from xml.dom import minidom
import os
import csv
def get_values(csv_file_path, target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        # Create a csv reader
        csvreader = csv.DictReader(csvfile)

        # Check if the target column is present in the header
        if target_column not in csvreader.fieldnames:
            print(f"Error: Column '{target_column}' not found in the csv file.")
        else:
            column_values = [row[target_column] for row in csvreader ]
            return column_values


def get_num_doc(csv_file_path):
    target_column = "Token ID"
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        # Create a csv reader
        csvreader = csv.DictReader(csvfile)
        # Check if the target column is present in the header
        if target_column not in csvreader.fieldnames:
            print(f"Error: Column '{target_column}' not found in the csv file.")
        else:
            column_values = [row[target_column] for row in csvreader ]
            return int(column_values[-1][1:4])

def get_num_sentences(csv_file_path, doc_num):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        # Create a csv reader
        csvreader = csv.DictReader(csvfile)
        # Check if the target column is present in the header
        column_values = [row["Token ID"] for row in csvreader ]
    doc = [x for x in column_values if x[0:4] == doc_num]
    return int(doc[-1][6:9])

def get_tokens(sentence_id, input_file,object,root):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        # Create a csv reader
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row["Token ID"][0:9] == sentence_id:
                token = root.createElement("wf")
                token.setAttribute("id",row["Token ID"])
                token.setAttribute("lemma", row["Lemma"])
                token.setAttribute("pos", row["POS"])
                x = root.createTextNode(row["Token"])
                token.appendChild(x)
                object.appendChild(token)


def GenerateXML(input_file,output_file,lang):
    root = minidom.Document()
    xml = root.createElement("corpus")
    xml.setAttribute('lang', lang)
    root.appendChild(xml)
    for x in range(1,get_num_doc(input_file)+1):
        docId = ""
        if x % 10 == x:
            docId = f"d00{x}"
        #add more here if we want to be general
        document = root.createElement('text')
        document.setAttribute('id', docId)
        xml.appendChild(document)
        num_sen = get_num_sentences(input_file,docId)
        for y in range(1,num_sen+1):
            if y % 10 == y:
                senId = f"s00{y}"
            else:
                senId = f"s0{y}"
            sentence = root.createElement("sentence")
            sentence.setAttribute('id',f"{docId}.{senId}")
            document.appendChild(sentence)
            get_tokens(f"{docId}.{senId}",input_file,sentence,root)
    xml_str = root.toprettyxml(indent="\t")
    with open(output_file, "w") as f:
        f.write(xml_str)


if __name__ == "__main__":
    lang = "EN"
    input_file = "out_tokens.csv"
    output_file = "output.xml"
    GenerateXML(input_file,output_file,lang)

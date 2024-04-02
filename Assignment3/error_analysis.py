import csv

data = []
annotator_note_dict = {}
total_sense = 0
correct_sense = 0
incorrect_sense = 0
synonym = 0
rows_without_sense = 0

with open("a3_tokens - ANNOTATION - Aligned (Farsi).csv", 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    next(reader)

    for _ in range(1605):
        next(reader)

    for row in reader:
        document_number = int(row[0].split('.')[0][1:])
        if document_number == 4:
            break
        data.append(row)

        babel_id = row[7]
        if babel_id != 'n/a':
            correctness = int(row[8])
            is_synonym = row[9]

            total_sense += 1

            if correctness == 1:
                correct_sense += 1

            if is_synonym != '' and correctness == 0 and int(is_synonym) == 1:
                synonym += 1

            annotator_note = row[12]
            if annotator_note != "":
                if annotator_note in annotator_note_dict.keys():
                    annotator_note_dict[annotator_note] += 1
                else:
                    annotator_note_dict[annotator_note] = 1
        else:
            rows_without_sense += 1

for key in annotator_note_dict:
    incorrect_sense += annotator_note_dict[key]

print(annotator_note_dict)

print(f"The annotator_note dictionary length: {len(annotator_note_dict)}")
print(f"The number of total sense: {total_sense}")
print(f"The number of rows without sense: {rows_without_sense}")
print(f"The number of correct sense tags: {correct_sense}")
print(f"The number of incorrect sense tags: {incorrect_sense}")
print(f"The number of rows with synonym: {synonym}")

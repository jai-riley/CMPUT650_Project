from scipy.stats import pearsonr, spearmanr
from get_score import get_values
import os
import csv

def eval():
    all_files = os.listdir("SemEval2024-Task1/outputTHM")
    all_files = ["esp_dev.csv"]
    for file in all_files:
        with open(f"{file}", 'w', newline='') as csvfile:

                lst = []
                #print(file[0:7])
                if file[0:7] == "track4a":
                    label = "SemEval2024-Task1/labels/track4a_sts_esp_eng_test_with_normlabels.csv"
                elif file[0:7] == "track4b":
                    label = "SemEval2024-Task1/labels/track4b_sts_esp_eng_test_with_normlabels.csv"
                elif file[-8:] == "test.csv" or file[4:8] == "test":
                    label = "SemEval2024-Task1/labels/" + file[0:3] + "_test_with_labels.csv"
                elif file[-7:] == "dev.csv" or file[4:7] == "dev":
                    label = "SemEval2024-Task1/labels/" + file[0:3] + "_dev_with_labels.csv"
                else:
                    label = "SemEval2024-Task1/labels/sts_eng_eng_test_with_normlabels.csv"

                output_file = "SemEval2024-Task1/outputTHM/" + file

                dev_ys = get_values(label, "Score")
                dev_ys_ = get_values(output_file, "Pred_Score")
                pearson, y = pearsonr(dev_ys, dev_ys_)
                spearman, y = spearmanr(dev_ys, dev_ys_)

                new_row = [spearman, pearson]
                # Open the CSV file in append mode
                    # Create a CSV writer object
                csv_writer = csv.writer(csvfile)

                    # Write the new row to the CSV file
                csv_writer.writerow(new_row)

# track 5: 0.70559414430069 0.7397057487960365
# track 4a: 0.706261167243184 0.6923441392897155
# track 4b: 0.1806613778143154 0.18207644425234684

# O - track 4b: 0.2223602297146475 0.194238978366608
# O - track 4a:

# afr: 0.5574056468123397 0.6472284206910139

# esp: 0.5728845332080186 0.585409019070367, 0.6336848736698238 0.6093109149031243
# eng: 0.6034921142245867 0.6311834090408295, 0.6443980601117393 0.633632195245917
eval()

import csv
def avg():
    all_files = os.listdir("eval_baseline")
    with open(f"final_random.csv", 'a', newline='') as csvf:
        cw = csv.writer(csvf)
        for file in all_files:
            column_index = 0  # For example, 1 corresponds to the second column (0-indexed)
            total_0 = 0
            total_1 = 0

            count = 0
            # Open the CSV file and calculate the sum and count for the specified column
            with open(f"eval_baseline/{file}", 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                #header = next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    try:
                        value = float(row[column_index])  # Convert the value to float
                        total_0 += value
                        value = float(row[column_index+1])  # Convert the value to float
                        total_1 += value
                        count += 1
                    except ValueError:
                        print(f"Invalid value in row {csv_reader.line_num}: {row[column_index]}")

            # Calculate the average
            if count > 0:
                #average = total_0 / count
                with open(f"eval_baseline/{file}", 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    new_row = [total_0 / count, total_1 / count]
                    csv_writer.writerow(new_row)
                    new_row = [file[5:], total_0 / count, total_1 / count]
                    cw.writerow(new_row)


#
#avg()
"""
# Specify the file path
file_path = 'random.csv'

# Specify the column index for which you want to calculate the average
column_index = 1  # For example, 1 corresponds to the second column (0-indexed)

# Initialize variables for sum and count
total = 0
count = 0

# Open the CSV file and calculate the sum and count for the specified column
with open(file_path, 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        try:
            value = float(row[column_index])  # Convert the value to float
            total += value
            count += 1
        except ValueError:
            print(f"Invalid value in row {csv_reader.line_num}: {row[column_index]}")

# Calculate the average
if count > 0:
    average = total / count
    print(f"The average of column {column_index} is: {average}")
else:
    print("No valid data found in the specified column.")

"""


from scipy.stats import pearsonr, spearmanr
from get_score import get_values
import os
import csv

all_dirs = os.listdir("SemEval2024-Task1/output")
dirs = []
for file in all_dirs:
    if file[-8:] == "test.csv":
        dirs.append(file)
#dirs.remove("eng_dev.csv")
# dirs.remove("eng_test.csv")
#dirs.remove("esp_dev.csv")
#dirs.remove("kin2eng_test.csv")
#dirs.remove("kin2eng_dev.csv")
#dirs.remove("afr2eng_dev.csv")
#dirs.remove("esp2eng_test.csv")
dirs = ["track5_eng_eng_test.csv"]
for file in dirs:
    print(file)
    lst = []
    if file[-8:] == "test.csv" or file[4:8] == "test":
        label = "SemEval2024-Task1/labels/" + file[0:3] + "_test_with_labels.csv"
    else:
        label = "SemEval2024-Task1/labels/" + file[0:3] + "_dev_with_labels.csv"

    output_file = "SemEval2024-Task1/output/" + file

    dev_ys = get_values("sts_eng_eng_test_with_normlabels.csv", "Score")
    dev_ys_ = get_values(output_file, "Pred_Score")
    print(len(dev_ys),len(dev_ys_))
    pearson, y = pearsonr(dev_ys, dev_ys_)
    spearman, y = spearmanr(dev_ys, dev_ys_)

    new_row = [file, "THM(0.8)", spearman, pearson]
    file_path = 'evaluation.csv'
    # Open the CSV file in append mode
    with open(file_path, 'a', newline='') as csvfile:
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
"""
import csv

# Specify the file path
file_path = 'evaluation.csv'

# Specify the column index for which you want to calculate the average
column_index = 3  # For example, 1 corresponds to the second column (0-indexed)

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

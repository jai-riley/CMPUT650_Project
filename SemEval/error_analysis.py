# create a csv file with PairID and then
# spearman correlation for each sentence pair for WO/CO
from get_score import get_values
from scipy.stats import pearsonr, spearmanr
import csv
wo_eng = get_values("eng_test.csv","Pred_Score")
co_eng = get_values("SemEval2024-Task1/outputTHM/eng_test.csv", "Pred_Score")
gold = get_values("SemEval2024-Task1/labels/eng_test_with_labels.csv", "Score")
sentences_1 = get_values("SemEval2024-Task1/eng_test.csv","Text")
#sentences_2 = get_values("sts/trans_track4b_sts_esp_eng_test.csv","Text2")

with open("comparison_eng_test.csv", mode='a', newline='') as file:
    writer = csv.writer(file)
    #writer.writerow(["PairID","gold","WO","CO"])
    for x in range(len(wo_eng)):
        if x % 10 == x:
            id = f'000{x}'
        elif x % 100 == x:
            id = f'00{x}'
        elif x % 1000 == x:
            id = f'0{x}'
        else:
            id = f'{x}'
        #a = f"{(gold[x] - wo_eng[x]):.2f}"
        #c = f"{(gold[x] - co_eng[x]):.2f}"
        #data = [f"ENG-test-{id}",gold[x],a,c]
        if (abs(gold[x]-wo_eng[x]*2) <= 0.1) and (abs(wo_eng[x]*2-co_eng[x]) >= 0.2):
            data = [f"ENG-test-{id}",gold[x],wo_eng[x]*2,co_eng[x],f"{sentences_1[x]}"]
            writer.writerow(data)

        # 43 wo is closer to correct -> 116 co is closer

from Simplified_Extended_Lesk import *
gold_standard = []
try:
    with open('subtask1-homographic-test.gold', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                gold_standard.append(line[len(line)- 1])
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    for index in range(2250):
        output = pun(dict1[index], dict2[index])
	gold = gold_standard[index]
	if(output == 'A pun!' and gold == '1'):
		TP += 1
	if(output == 'A pun!' and gold == '0'):
		FP += 1
	if(output == 'Not a pun!' and gold == '1'):
		FN += 1
	if(output == 'Not a pun!' and gold == '0'):
		TN += 1

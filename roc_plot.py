import math
import operator
data = open("data5.txt",'w')

for threshold in range(0, 101, 1):
    posi_num = 0
    true_posi_num = 0
    nega_num = 0
    false_posi_num = 0
    threshold = float(threshold) / 100
    print threshold
    for line in open("roc_dataset_bayes_rl.txt", 'r'):
        first_line_str_list = line.replace("\n", "").split("\t")
        temp_str_list = first_line_str_list[1].split('_aaa_')
        if temp_str_list[0] == '1':
            posi_num = posi_num + 1
            if float(first_line_str_list[2]) > threshold:
                true_posi_num = true_posi_num + 1
        else:
            nega_num = nega_num + 1
            if float(first_line_str_list[2]) > threshold:
                false_posi_num = false_posi_num + 1
    #print float(posi_num) / (posi_num + nega_num)
    false_posi_rate = float(false_posi_num) / nega_num
    true_posi_rate = float(true_posi_num) / posi_num
    data.write(str(false_posi_rate) + '\t' + str(true_posi_rate) + '\n')

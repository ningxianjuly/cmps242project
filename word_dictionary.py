'''
Created on 2 Nov, 2016

@author: luotianyi
'''
import json

if __name__ == '__main__':
    dataset_file_location = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'traindata_20161103'
    f_write_dataset_pos = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_pos_frequency_40000_20161102', 'w')
    f_write_dataset_neg = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_neg_frequency_40000_20161102', 'w')
    #print dataset_file_location
    line_num_int = 0 #number of line
    word_diction_pos = {} #word dictionary of positive samples
    word_diction_neg = {} #word dictionary of positive samples
    word_pos_num = 0 #number of words in the positive samples
    word_neg_num = 0 #number of words in the negative samples
    word_distinct_pos_num = 0 #number of distinct words in the positive samples
    word_distinct_neg_num = 0 #number of distinct words in the negtive samples
    sentence_pos_num = 0 #number of positive samples
    sentence_neg_num = 0 #number of negtive samples
    for line in open(dataset_file_location, 'r'):
        line_num_int += 1
        if line_num_int % 5000 == 0:
            print str(line_num_int) + " lines are handled"
        temp_str_arraylist = line.split("\t")
        temp_text = temp_str_arraylist[1].replace("\n", "")
        temp_label = int(temp_str_arraylist[0])
        temp_text_arraylist = temp_text.split(" ")
        if temp_label == 1:
            sentence_pos_num += 1
        else:
            sentence_neg_num += 1
        for word in temp_text_arraylist:
            if temp_label == 1:
                word_pos_num += 1
                if word + "_pos" not in word_diction_pos:
                    word_distinct_pos_num +=1
                    word_diction_pos[word + "_pos"] = 1
                else:
                    word_diction_pos[word + "_pos"] += 1
            else:
                word_neg_num += 1
                if word + "_neg" not in word_diction_neg:
                    word_distinct_neg_num +=1
                    word_diction_neg[word + "_neg"] = 1
                else:
                    word_diction_neg[word + "_neg"] += 1
    f_write_dataset_pos.write(str(sentence_pos_num) + "\t" + str(word_distinct_pos_num) + "\t" + str(word_pos_num) + "\n")
    for word_write_pos in word_diction_pos.keys():
        if word_diction_pos[word_write_pos] >= 10000:
            f_write_dataset_pos.write(word_write_pos + "\t" + str(word_diction_pos[word_write_pos]) + "\n")
    f_write_dataset_neg.write(str(sentence_neg_num) + "\t" + str(word_distinct_neg_num) + "\t" + str(word_neg_num) + "\n")
    for word_write_neg in word_diction_neg.keys(): 
        if word_diction_neg[word_write_neg] >= 10000:
            f_write_dataset_neg.write(word_write_neg + "\t" + str(word_diction_neg[word_write_neg]) + "\n")
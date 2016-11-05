'''
Created on 2 Nov, 2016

@author: luotianyi
'''
import json

if __name__ == '__main__':
    dataset_file_location = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'traindata_20161103'
    f_write_dataset = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_all_frequency_40000_20161105', 'w')
    #print dataset_file_location
    line_num_int = 0 #number of line
    word_diction = {} #word dictionary of positive samples

    for line in open(dataset_file_location, 'r'):
        line_num_int += 1
        if line_num_int % 5000 == 0:
            print str(line_num_int) + " lines are handled"
        temp_str_arraylist = line.split("\t")
        temp_text = temp_str_arraylist[1].replace("\n", "")
        temp_label = int(temp_str_arraylist[0])
        temp_text_arraylist = temp_text.split(" ")

        for word in temp_text_arraylist:
            if word not in word_diction:
                word_diction[word] = 1
            else:
                word_diction[word] += 1
                    
    for word_write in word_diction.keys():
        if word_diction[word_write] >= 5000 and len(word_write) >= 1:
            f_write_dataset.write(word_write + "\t" + str(word_diction[word_write]) + "\n")
    
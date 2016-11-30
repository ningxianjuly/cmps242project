'''
Created on 3 Nov, 2016

@author: luotianyi
'''
#Naive Bayes
import numpy
from collections import OrderedDict


if __name__ == '__main__':
    file_dataset_pos = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_pos_frequency_40000_20161102'
    file_dataset_neg = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_neg_frequency_40000_20161102'
    file_dataset_train = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'traindata_20161103'
    file_dataset_test = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'testdata_20161103'
    sentence_pos_num = 0 #number of positive samples
    sentence_neg_num = 0 #number of negtive samples
    word_distinct_pos_num = 0 #number of distinct words in the positive samples
    word_distinct_neg_num = 0 #number of distinct words in the negtive samples
    word_pos_num = 0 #number of words in the positive samples
    word_neg_num = 0 #number of words in the negative samples
    word_diction_pos = {} #word dictionary of positive samples
    word_diction_neg = {} #word dictionary of positive samples
    line_pos_num = 0
    line_neg_num = 0
    trainset_num = 27716
    train_right_num = 0
    testset_num = 6000
    test_right_num = 0
    for pos_line in open(file_dataset_pos, 'r'):
        line_pos_num += 1
        if line_pos_num == 1:
            first_line_str_list = pos_line.replace("\n", "").split("\t")
            sentence_pos_num = int(first_line_str_list[0])
            word_distinct_pos_num = int(first_line_str_list[1])
            word_pos_num = int(first_line_str_list[2])
        else:
            not_first_line_str_list = pos_line.replace("\n", "").split("\t")
            word_diction_pos[not_first_line_str_list[0]] = not_first_line_str_list[1]
            
    for neg_line in open(file_dataset_neg, 'r'):
        line_neg_num += 1
        if line_neg_num == 1:
            first_line_str_list = neg_line.replace("\n", "").split("\t")
            sentence_neg_num = int(first_line_str_list[0])
            word_distinct_neg_num = int(first_line_str_list[1])
            word_neg_num = int(first_line_str_list[2])
        else:
            not_first_line_str_list = neg_line.replace("\n", "").split("\t")
            word_diction_neg[not_first_line_str_list[0]] = not_first_line_str_list[1]

    #calculate the classification accuracy of training dataset
    prob_class_pos = 1.0 * sentence_pos_num / (sentence_pos_num + sentence_neg_num)
    prob_class_neg = 1.0 * sentence_neg_num / (sentence_pos_num + sentence_neg_num)
    line_train_num = 0
    for train_line in open(file_dataset_train, 'r'):
        line_train_num += 1
        if line_train_num % 5000 == 0:
            print str(line_train_num) + " lines are handled" 
        temp_list = train_line.replace("\n", "").split("\t")
        temp_label = int(temp_list[0])
        temp_text = temp_list[1].replace("\n", "").split(" ")
        prob_pos = 1.0
        prob_neg = 1.0
        for word in temp_text:
            if word + "_pos" in word_diction_pos:
                #laplace smoothing
                prob_pos += numpy.log(10000.0 *(int(word_diction_pos[word + "_pos"]) + 1)/(word_pos_num + word_distinct_pos_num))
            else:
                prob_pos += numpy.log(10000.0/(word_pos_num + word_distinct_pos_num))
            if word + "_neg" in word_diction_neg:
                #laplace smoothing
                prob_neg += numpy.log(10000.0 *(int(word_diction_neg[word + "_neg"]) + 1)/(word_neg_num + word_distinct_neg_num))
            else:
                prob_neg += numpy.log(10000.0/(word_neg_num + word_distinct_neg_num))
        prob_pos += numpy.log(prob_class_pos)
        prob_neg += numpy.log(prob_class_neg)
        if prob_pos >= prob_neg and temp_label == 1:
            train_right_num += 1
        if prob_pos < prob_neg and temp_label == 0:
            train_right_num += 1
    print "The classification accuracy of train dataset is:"
    print 1.0 * train_right_num / trainset_num
    
    #calculate the classification accuracy of test dataset
    line_test_num = 0
    f_write_dataset_test = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'roc_dataset', 'w')
    temp_dic = {}
    for test_line in open(file_dataset_test, 'r'):
        line_test_num += 1
        if line_test_num % 5000 == 0:
            print str(line_test_num) + " lines are handled" 
        temp_list = test_line.replace("\n", "").split("\t")
        temp_label = int(temp_list[0])
        temp_text = temp_list[1].replace("\n", "").split(" ")
        prob_pos = 1.0
        prob_neg = 1.0
        for word in temp_text:
            if word + "_pos" in word_diction_pos:
                #laplace smoothing
                prob_pos += numpy.log(1.0 *(int(word_diction_pos[word + "_pos"]) + 1)/(word_pos_num + word_distinct_pos_num))
            else:
                prob_pos += numpy.log(1.0/(word_pos_num + word_distinct_pos_num))
            if word + "_neg" in word_diction_neg:
                #laplace smoothing
                prob_neg += numpy.log(1.0 *(int(word_diction_neg[word + "_neg"]) + 1)/(word_neg_num + word_distinct_neg_num))
            else:
                prob_neg += numpy.log(1.0/(word_neg_num + word_distinct_neg_num))
        prob_pos += numpy.log(prob_class_pos)
        prob_neg += numpy.log(prob_class_neg)
        #######################################################
        temp_pos = 1.0 / (1.0 + numpy.power(2, prob_neg - prob_pos))
        temp_neg = 1.0 / (1.0 + numpy.power(2, prob_pos - prob_neg))
        temp_dic[str(temp_label) + "_aaa_" + str(line_test_num)] = temp_pos
        #######################################################
        if prob_pos >= prob_neg and temp_label == 1:
            test_right_num += 1
        if prob_pos < prob_neg and temp_label == 0:
            test_right_num += 1
    #sorted_d = OrderedDict(sorted(temp_dic.items(), key=lambda x: x[1]))
    #######################################################
    sorted_d = OrderedDict(sorted(temp_dic.items(), key=lambda x: x[1], reverse=True))
    num_write_line = 0
    for item_sorted in sorted_d:
        num_write_line += 1
        f_write_dataset_test.write(str(num_write_line) + "\t" + str(item_sorted) + "\t" + str(sorted_d[item_sorted]) + "\n")
    #######################################################
    print "The classification accuracy of test dataset is(Naive Bayes):"
    print 1.0 * test_right_num / testset_num

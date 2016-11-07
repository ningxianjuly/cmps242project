import time
import operator
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer
import math

def kNNClassify(item_x_test, train_dataSet_array, train_ylabels_array, K):  
    num_dataset = train_dataSet_array.shape[0] 
  
    #Calculate the Euclidean distance  
    subtract_test_train = tile(item_x_test, (num_dataset, 1)) - train_dataSet_array   
    square_subtract_test_train = subtract_test_train ** 2 
    squared_distance = sum(square_subtract_test_train, axis = 1)   
    euclidean_distance = sqrt(squared_distance)
   
    # argsort() returns the indices of a ascending order  
    indices_ascending = argsort(euclidean_distance)
  
    temp_count_dic_K = {} 
    for i in range(K):   
        temp_label = train_ylabels_array[indices_ascending[i]]
        if temp_label not in temp_count_dic_K:
            temp_count_dic_K[temp_label] = 1
        else:
            temp_count_dic_K[temp_label] += 1
   
    max_count = 0
    max_index = 0
    for key, value in temp_count_dic_K.items():  
        if value > max_count:  
            max_count = value
            max_index = key
  
    return max_index

if __name__ == '__main__':
    """ initialize parameters """
    
    file_dataset_word_frequency = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_all_frequency_40000_20161105'
    file_dataset_train = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'traindata_20161103'
    file_dataset_test = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'testdata_20161103'
    word_diction = {} #word dictionary
    line_num = 0
    for line in open(file_dataset_word_frequency, 'r'):
        line_num += 1
        line_str_list = line.replace("\n", "").split("\t")
        word_diction[line_str_list[0]] = line_str_list[1]

    #construct the vector representation with the feature of naive bayes
    train_vectors = []
    test_vectors = []
    ylabels_train = []
    labels = []
    add_labels = []
    test_ylabels = []
    line_num = 0
    #####################################
    #train tfidf feature construction
    #####################################
    for line in open(file_dataset_train, 'r'):
        line_num += 1
        if line_num % 5000 == 0:
            print "Triansets-" + str(line_num) + " lines are handled"
        #print "train_" + str(line_num)
        line_str_list = line.replace("\n", "").split("\t")
        temp_words_feature = []
        temp_text = line_str_list[1]
        ylabels_train.append(line_str_list[0])
        temp_words_list = temp_text.split(" ")
        for temp_word in word_diction:
            if line_num == 1:
                labels.append(temp_word)
            if str(temp_word) in temp_words_list:
                temp_words_feature.append(1.0 * (int(temp_words_list.count(str(temp_word)))))
            else:
                temp_words_feature.append(0.0)
        train_vectors.append(array(temp_words_feature))
    train_vectors_matrix = array(train_vectors)
    #print train_vectors_matrix[0]
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf_train = transformer.fit_transform(train_vectors_matrix)
    train_tfidf_array = tfidf_train.toarray()
    train_ylabels_array = array(ylabels_train)
    print "Train tfidf feature construction finish!"
    #####################################
    #test tfidf feature construction
    #####################################
    line_num = 0
    for line in open(file_dataset_test, 'r'):
        line_num += 1
        if line_num % 5000 == 0:
            print "Testsets-" + str(line_num) + " lines are handled"
        #print "test_" + str(line_num)
        line_str_list = line.replace("\n", "").split("\t")
        temp_words_feature = []
        temp_text = line_str_list[1]
        test_ylabels.append(line_str_list[0])
        temp_words_list = temp_text.split(" ")
        for temp_word in word_diction:
            if line_num == 1:
                add_labels.append(temp_word)
            if str(temp_word) in temp_words_list:
                temp_words_feature.append(1.0 * (int(temp_words_list.count(str(temp_word)))))
            else:
                temp_words_feature.append(0.0)
        test_vectors.append(array(temp_words_feature))
    test_vectors_matrix = array(test_vectors)
    #print test_vectors_matrix[0]
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf_test = transformer.fit_transform(test_vectors_matrix)
    test_tfidf_array = tfidf_test.toarray()
    test_ylabels_array = array(test_ylabels)
    print "Test tfidf feature construction finish!"
    print labels
    #print len(labels)
    #####################################
    #train dataset tranformation of decision tree
    #####################################
    train_dataSet = []
    for index_dataset in range(len(train_ylabels_array)):
        temp_single_dataset = []
        temp_dataset = train_tfidf_array[index_dataset]
        for index_temp_dataset in range(len(temp_dataset)):
            temp_single_dataset.append(temp_dataset[index_temp_dataset])
        #if train_ylabels_array[index_dataset] == '1':
        #    temp_single_dataset.append(1)
        #else:
        #    temp_single_dataset.append(-1)            
        train_dataSet.append(temp_single_dataset)
    #####################################
    #test dataset tranformation of decision tree
    #####################################
    test_dataSet = []
    for index_dataset in range(len(test_ylabels_array)):
        temp_single_dataset = []
        temp_dataset = test_tfidf_array[index_dataset]
        for index_temp_dataset in range(len(temp_dataset)):
            temp_single_dataset.append(temp_dataset[index_temp_dataset])    
        #if test_ylabels_array[index_dataset] == '1':
        #    temp_single_dataset.append(1)
        #else:
        #    temp_single_dataset.append(-1)       
        test_dataSet.append(temp_single_dataset)
    #####################################
    #train the perception
    #####################################
    #no training
    #####################################
    #test the perception
    #####################################
    K = 10
    print "Predicting..."
    test_right_num = 0
    line_test = 0
    for index_item_x_test in range(len(test_dataSet)):
        line_test += 1
        print line_test
        item_x_test = test_dataSet[index_item_x_test]
        label_test = test_ylabels_array[index_item_x_test]
        train_dataSet_array = array(train_dataSet)
        y_test = kNNClassify(item_x_test, train_dataSet_array, train_ylabels_array, K)
        if label_test == y_test:
            test_right_num += 1
    print "Predicting is finished!"
    print "The classification accuracy of test dataset is(perception):"
    print 1.0 * test_right_num / len(test_dataSet)

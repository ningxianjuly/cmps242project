'''
Created on 5 Nov, 2016

@author: luotianyi
'''
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer
import math

def cal_sigmoid(train_tfidf_array_index_X, initial_theta):
    linear_multiply_value = 0.0
    sigmoid_value = 0.0
    for index_X in range(len(train_tfidf_array_index_X)):
        linear_multiply_value += train_tfidf_array_index_X[index_X] * initial_theta[index_X]
    sigmoid_value = 1.0 / (1.0 + math.exp(-1.0*linear_multiply_value))
    return sigmoid_value

def delta_theta(alpha, train_tfidf_array, ylabels_array, initial_theta, index_theta):
    delta_value = 0.0
    for index_X in range(len(train_tfidf_array)):
        xij = train_tfidf_array[index_X][index_theta]
        delta_value += alpha * (float(ylabels_array[index_X])-cal_sigmoid(train_tfidf_array[index_X], initial_theta)) * xij
    return delta_value

def update_theta(alpha, train_tfidf_array, ylabels_array, initial_theta):
    updated_theta = []
    #sigmoid_value = cal_sigmoid(train_tfidf_array, ylabels_array)
    for index_theta in range(len(initial_theta)):
        updated_theta_index = initial_theta[index_theta] + delta_theta(alpha, train_tfidf_array, ylabels_array, initial_theta, index_theta)
        updated_theta.append(updated_theta_index)
    return updated_theta

def cost_value(train_tfidf_array, ylabels_array, updated_theta):
    total_errors = 0.0
    for index_X in range(len(train_tfidf_array)):
        error = 0.0
        train_tfidf_array_index_X = train_tfidf_array[index_X]
        sigmoid_value_index_X = cal_sigmoid(train_tfidf_array_index_X, updated_theta)
        if ylabels_array[index_X] == '1':
            error = math.log(sigmoid_value_index_X)
        elif ylabels_array[index_X] == '0':
            error = math.log(1-sigmoid_value_index_X)
        total_errors += error
    error_final = -1.0/len(ylabels_array) * total_errors
    return error_final



if __name__ == '__main__':
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
    initial_theta = []
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
                initial_theta.append(1.0)
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

    
    #train the logistic regression
    #initial_theta = [0, 0]
    alpha = 10.0 / len(train_ylabels_array)
    iterations_num = 10000
    line_num_iteration = 0
    updated_theta = 0.0
    for index_iteration in range(iterations_num):
        line_num_iteration += 1
        if line_num_iteration == 1:
            updated_theta_last = update_theta(alpha, train_tfidf_array, train_ylabels_array, initial_theta)
            updated_theta = updated_theta_last
        else:
            updated_theta_last = update_theta(alpha, train_tfidf_array, train_ylabels_array, updated_theta)
            updated_theta = updated_theta_last
        error_final = cost_value(train_tfidf_array, train_ylabels_array, updated_theta)
        print "The cost of " + str(index_iteration) + " iterations is " + str(error_final) + "."
    
        #test the performance of logistic regression
        print "Predicting..."
        predict_test_labels = []
        item_num = 0
        test_right_num = 0
        for item_test in test_tfidf_array:
            item_num += 1
            predict_test_prob = cal_sigmoid(item_test, updated_theta)
            if predict_test_prob >= 0.5 and test_ylabels_array[item_num - 1] == '1':
                test_right_num += 1
            if predict_test_prob < 0.5 and test_ylabels_array[item_num - 1] == '0':
                test_right_num += 1
            #print predict_test_labels
        print "Predicting is finished!"
        print "The classification accuracy of test dataset is(Logistic Regression):"
        print 1.0 * test_right_num / len(test_ylabels_array)

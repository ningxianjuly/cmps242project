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
    for index_X in range(train_tfidf_array_index_X):
        linear_multiply_value += train_tfidf_array_index_X[index_X] * initial_theta[index_X]
    sigmoid_value = 1.0 / (1.0 + math.exp(-1.0*linear_multiply_value))
    return sigmoid_value

def delta_theta(alpha, train_tfidf_array, ylabels_array, initial_theta, index_theta):
    delta_value = 0.0
    for index_X in range(train_tfidf_array):
        xij = train_tfidf_array[index_X][index_theta]
        delta_value += alpha * (ylabels_array[index_X]-cal_sigmoid(train_tfidf_array[index_X], initial_theta)) * xij
    return delta_value

def update_theta(alpha, train_tfidf_array, ylabels_array, initial_theta):
    updated_theta = []
    sigmoid_value = cal_sigmoid(train_tfidf_array, ylabels_array)
    for index_theta in range(initial_theta):
        updated_theta[index_theta] = initial_theta[index_theta] + delta_theta(train_tfidf_array, ylabels_array, initial_theta, index_theta)
    return updated_theta

def cost_value(train_tfidf_array, ylabels_array, updated_theta):
    total_errors = 0.0
    for index_X in range(len(train_tfidf_array)):
        error = 0.0
        train_tfidf_array_index_X = train_tfidf_array[index_X]
        sigmoid_value_index_X = cal_sigmoid(train_tfidf_array_index_X, updated_theta)
        if ylabels_array[index_X] == 1:
            error = math.log(sigmoid_value_index_X)
        elif ylabels_array[index_X] == 0:
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
    trainset_num = 40000
    train_right_num = 0
    testset_num = 10000
    test_right_num = 0
    for line in open(file_dataset_word_frequency, 'r'):
        line_num += 1
        line_str_list = line.replace("\n", "").split("\t")
        word_diction[line_str_list[0]] = line_str_list[1]
    
    #construct the vector representation with the feature of naive bayes
    train_vectors = []
    test_vectors = []
    ylabels = []
    line_num = 0
    for line in open(file_dataset_train, 'r'):
        line_num += 1
        print line_num
        line_str_list = line.replace("\n", "").split("\t")
        temp_words_feature = []
        temp_text = line_str_list[1]
        ylabels.append(line_str_list[0])
        temp_words_list = temp_text.split(" ")
        for temp_word in word_diction:
            if str(temp_word) in temp_words_list:
                temp_words_feature.append(1.0 * (int(temp_words_list.count(str(temp_word)))))
            else:
                temp_words_feature.append(0.0)
        train_vectors.append(array(temp_words_feature))
    train_vectors_matrix = array(train_vectors)
    print train_vectors_matrix[0]
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(train_vectors_matrix)
    
    #train the logistic regression
    train_tfidf_array = tfidf.toarray()
    ylabels_array = ylabels.toarray()
    initial_theta = [0, 0]
    alpha = 0.1 / len(ylabels_array)
    iterations_num = 10000
    for index_iteration in iterations_num:
        updated_theta = update_theta(alpha, train_tfidf_array, ylabels_array, initial_theta)
        error_final = cost_value(train_tfidf_array, ylabels_array, updated_theta)
        print "The cost of " + str(index_iteration) + " iterations is " + str(error_final) + "."
    
    #test the performance of logistic regression
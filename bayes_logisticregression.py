'''
Created on 7 Nov, 2016

@author: luotianyi
'''
import numpy
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer
import math
from scipy.optimize import minimize
from collections import OrderedDict

def cal_sigmoid(X, w):
    linear_multiply_value = numpy.dot(X, w)
    exp_prob = numpy.exp(linear_multiply_value)
    sigmoid_value = exp_prob / (1.0 + exp_prob)
    return sigmoid_value

def cost(w, w_prior, H, y_temp, X_temp):
    X = numpy.array(X_temp,dtype=float)
    y = numpy.array(y_temp,dtype=float)
    mu = cal_sigmoid(X, w)
    #temp_x = numpy.dot(y.T, numpy.log(mu))
    #print temp_x
    cost_value = (-(numpy.dot(y.T, numpy.log(mu)) + numpy.dot((1.0 - y).T, numpy.log(1.0 - mu)))
                        + 0.5 * numpy.dot((w - w_prior).T, numpy.dot(H, (w - w_prior))))
    return cost_value
    
def gradient(w, w_prior, H, y_temp, X_temp):
    X = numpy.array(X_temp,dtype=float)
    y = numpy.array(y_temp,dtype=float)
    mu = cal_sigmoid(X, w)
    gradient_value = numpy.dot(X.T, (mu - y)) + numpy.dot(H, (w - w_prior))
    return gradient_value
    
def hessian(w, w_prior, H, y, X):    
    mu = cal_sigmoid(X, w)
    S = mu * (1.0 - mu)
    hessian_value = numpy.dot(X.T, X * S[:, numpy.newaxis]) + H
    return hessian_value
    
def fit_bayes_logistic(y, X, w_prior, H, max_iterartions):
    results_optimize = minimize(cost, w_prior, args=(w_prior, H, y, X), jac=gradient, hess=hessian, method='Newton-CG', options={'maxiter': max_iterartions})
    w_fit = results_optimize.x
    H_fit = hessian(w_fit, w_prior, H, y, X)
    return w_fit, H_fit

def predict_bayes_logistic_prob(X, w, H):
    linear_multiply_value_pre = numpy.dot(X, w)
    hessian_inverse = numpy.linalg.inv(H)
    variance = numpy.sum(X * numpy.dot(hessian_inverse, X.T).T, axis=1)
    kappa_variance = 1.0 / numpy.sqrt(1. + 0.125 * numpy.pi * variance)
    linear_multiply_value = linear_multiply_value_pre * kappa_variance
    exp_prob = numpy.exp(linear_multiply_value)
    sigmoid_value = exp_prob / (1.0 + exp_prob)
    return sigmoid_value

if __name__ == '__main__':
    file_dataset_word_frequency = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'word_all_frequency_40000_20161105'
    #file_dataset_train = '/Users/luotianyi/Desktop/CMPS242/project/'\
    #'traindata_hw3'
    #file_dataset_test = '/Users/luotianyi/Desktop/CMPS242/project/'\
    #'testdata_hw3'
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
                #####################################
                initial_theta.append(1.0)
                #####################################
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
    
    #train the bayes logistic regression
    w_prior = initial_theta#numpy.zeros(len(word_diction))
    H_prior = numpy.diag(numpy.ones(len(word_diction)))*0.001 #* 100.0
    w_posterior, H_posterior = fit_bayes_logistic(train_ylabels_array, train_tfidf_array, w_prior, H_prior, 5000)
    print w_posterior
    print H_posterior
    
    #get the performance of train utilizing bayes logistic regression
    print "Predicting training dataset..."
    predict_train_prob_array = predict_bayes_logistic_prob(train_tfidf_array, w_posterior, H_posterior)
    predict_train_labels = []
    item_num = 0
    train_right_num = 0
    for item_test in train_tfidf_array:
        item_num += 1
        predict_train_prob = predict_train_prob_array[item_num - 1]
        if predict_train_prob >= 0.5 and train_ylabels_array[item_num - 1] == '1':
            train_right_num += 1
        if predict_train_prob < 0.5 and train_ylabels_array[item_num - 1] == '0':
            train_right_num += 1
        #print predict_test_labels
    print "Predicting training dataset is finished!"
    print "The classification accuracy of train dataset is(Bayes Logistic Regression):"
    print 1.0 * train_right_num / len(train_ylabels_array)
    
    #get the performance of test utilizing bayes logistic regression
    print "Predicting test dataset..."
    predict_test_prob_array = predict_bayes_logistic_prob(test_tfidf_array, w_posterior, H_posterior)
    predict_test_labels = []
    item_num = 0
    test_right_num = 0
    temp_dic = {}
    f_write_dataset_test = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'roc_dataset_bayes_lr', 'w')
    for item_test in test_tfidf_array:
        item_num += 1
        predict_test_prob = predict_test_prob_array[item_num - 1]
        if predict_test_prob >= 0.5 and test_ylabels_array[item_num - 1] == '1':
            test_right_num += 1
        if predict_test_prob < 0.5 and test_ylabels_array[item_num - 1] == '0':
            test_right_num += 1
        #######################################################
        temp_pos = predict_test_prob
        temp_dic[test_ylabels_array[item_num - 1] + "_aaa_" + str(item_num)] = temp_pos
        #######################################################
        #print predict_test_labels
    #######################################################
    sorted_d = OrderedDict(sorted(temp_dic.items(), key=lambda x: x[1], reverse=True))
    num_write_line = 0
    for item_sorted in sorted_d:
        num_write_line += 1
        f_write_dataset_test.write(str(num_write_line) + "\t" + str(item_sorted) + "\t" + str(sorted_d[item_sorted]) + "\n")
    #######################################################
    print "Predicting test dataset is finished!"
    print "The classification accuracy of test dataset is(Bayes Logistic Regression):"
    print 1.0 * test_right_num / len(test_ylabels_array)

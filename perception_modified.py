import time
import operator
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer
import math

""" Given input X, compute output """
def predict_result (X, W, b, learning_rate):
    y = 0.0
    for index in range(len(X)):
        y += W[index] * X[index] 
    y += b
    if y > 0.0 :
        return 1;
    else :
        return -1;

def train (train_dataSet, W, b, learning_rate):
    ''' iterate at most 1000 times '''   
    for i in range (1, 10000) : 
        print i
        error = 0.0
        for item_x in train_dataSet: 
            X = item_x[0:len(item_x) - 1]
            label = item_x[len(item_x) - 1]
            y = predict_result(X, W, b, learning_rate)
            #if y is misclassified, we update the weights
            if label != y :
                error +=  1
                y = 0.0
                for index in range(len(X)):
                    y += W[index] * X[index]
                    W[index] = W[index] + learning_rate * label * X[index]
                b = b + learning_rate * label  
            #print "W:" + str(W)
            #print "b:" + str(b)   
        print "The number of error:" + str(error)   
        if error == 0 :
            break
    return W, b

if __name__ == '__main__':
    """ initialize parameters """
    W = []
    b = 0
    learning_rate = 0.01
    
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
    for item_w in range(len(word_diction)):
        W.append(1)
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
        if train_ylabels_array[index_dataset] == '1':
            temp_single_dataset.append(1)
        else:
            temp_single_dataset.append(-1)            
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
        if test_ylabels_array[index_dataset] == '1':
            temp_single_dataset.append(1)
        else:
            temp_single_dataset.append(-1)       
        test_dataSet.append(temp_single_dataset)
    #####################################
    #train the perception
    #####################################
    print "Training..."
    trained_W, trained_b = train(train_dataSet, W, b, learning_rate)
    print "Training is finished!"
    #####################################
    #test the perception
    #####################################
    print "Predicting..."
    test_right_num = 0
    for item_x_test in test_dataSet: 
        X_test = item_x_test[0:len(item_x_test) - 1]
        label_test = item_x_test[len(item_x_test) - 1]
        y_test = predict_result(X_test, trained_W, trained_b, learning_rate)
        if label_test == y_test:
            test_right_num += 1
    print "Predicting is finished!"
    print "The classification accuracy of test dataset is(perception):"
    print 1.0 * test_right_num / len(test_dataSet)

'''
Created on 5 Nov, 2016

@author: luotianyi
'''
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer

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
    line_num = 0
    for line in open(file_dataset_train, 'r'):
        line_num += 1
        print line_num
        line_str_list = line.replace("\n", "").split("\t")
        temp_words_feature = []
        temp_text = line_str_list[1]
        temp_words_list = temp_text.split(" ")
        #index_word = 0
        for temp_word in word_diction:
            #index_word += 1
            #print index_word
            if str(temp_word) in temp_words_list:
                temp_words_feature.append(1.0 * (int(temp_words_list.count(str(temp_word)))))
                #print 1.0 * (int(temp_words_list.count(str(temp_word))))
            else:
                temp_words_feature.append(0.0)
        train_vectors.append(array(temp_words_feature))
    train_vectors_matrix = array(train_vectors)
    #print type(train_vectors_matrix)
    print train_vectors_matrix[0]
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(train_vectors_matrix)
    print tfidf.toarray()[0]
    
    #train the logistic regression
    

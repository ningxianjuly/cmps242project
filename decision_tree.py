import math
import operator
from numpy import *
from sklearn.feature_extraction.text import TfidfTransformer
import math

def calcShannonEnt(dataSet): #calculate the shannon value
    numEntries = len(dataSet) #calculate the total number of input data
    labelCounts = {}
    for featVec in dataSet:      #create the dictionary for all of the data
        currentLabel = featVec[-1] #the last element is the label
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts: #for different label, calculate it's shannon value
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob*math.log(prob,2) #combine all the caculated value to gain the shannon value for this feature
    return shannonEnt

def createDataSet(): #the dataset, This is the main problem because I have not used the Yelp data
    
    dataSet = [[1,1,1,'yes'],
               [1,1,0,'yes'],
               [1,0,1,'no'],
               [0,1,0,'yes'],
               [0,1,0,'no']]
    labels = ['Good','Bad','Delicious']
    return dataSet, labels

def splitDataSet(dataSet, axis, value): #to obtain the dataset with selected feature and value
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis] #delete the selected value since we have handled it
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet): #find the best feature to decide
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)   #convert from list to set to get the unique value
        newEntropy = 0.0
        for value in uniqueVals: #caculate the entrop for this feature
            subDataSet = splitDataSet(dataSet, i , value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy +=prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList): #Find the majority class when all the features have been used
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]     # the type is the same, so stop classify
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if (len(dataSet[0]) == 1):  # all the features have been used
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat]) #In splitDataSet, we have deleted the feature,so the label should be deleted too
    #get the list which attain the whole properties
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals: #use the recurrence to get the tree
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec): #Travers the decision tree to get the result
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = 'yes'
    #classLabels = []
    #for testVec in testVecs:
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
                #classLabels.append(classLabel)
            else: 
                classLabel = secondDict[key]
                #classLabels.append(classLabel)
    #print classLabel
    return classLabel

if __name__ == '__main__':
    #if '1' == '1':
    #    print "Rubbish!"
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
            if temp_dataset[index_temp_dataset] >= 0.5:
                temp_single_dataset.append(1)
            else:
                temp_single_dataset.append(0)
        if train_ylabels_array[index_dataset] == '1':
            temp_single_dataset.append('yes')
        else:
            temp_single_dataset.append('no')            
        train_dataSet.append(temp_single_dataset)
    #####################################
    #test dataset tranformation of decision tree
    #####################################
    test_dataSet = []
    for index_dataset in range(len(test_ylabels_array)):
        temp_single_dataset = []
        temp_dataset = test_tfidf_array[index_dataset]
        for index_temp_dataset in range(len(temp_dataset)):
            if temp_dataset[index_temp_dataset] >= 0.5:
                temp_single_dataset.append(1)
            else:
                temp_single_dataset.append(0)
        #if test_ylabels_array[index_dataset] == '1':
        #    temp_single_dataset.append('yes')
        #else:
        #    temp_single_dataset.append('no')            
        test_dataSet.append(temp_single_dataset)
    #####################################
    #get the performance of test dataset
    #####################################
    test_right_num = 0
    print "Creating tree..."
    #print len(labels)
    myTree = createTree(train_dataSet,labels)
    print "Creating tree is finished!"
    print "Predicting..."
    predict_test_labels = []
    item_num = 0
    for item_test in test_dataSet:
        item_num += 1
        #print item_test
        temp_labels = add_labels
        #print len(temp_labels)
        predict_test_label = classify(myTree,temp_labels,item_test)
        if predict_test_label == 'yes':
            predict_test_labels.append('1')
        else:
            predict_test_labels.append('0')
        #print predict_test_labels
    print "Predicting is finished!"
    predict_test_labels_array = array(predict_test_labels)
    for index_item_label in range(len(test_ylabels_array)):
        if test_ylabels_array[index_item_label] == predict_test_labels_array[index_item_label]:
            test_right_num += 1
    print "The classification accuracy of test dataset is(decision_tree):"
    print 1.0 * test_right_num / len(test_ylabels_array)

import math
import operator

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
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else: classLabel = secondDict[key]
    return classLabel

myDat, labels = createDataSet()
myTree = createTree(myDat,labels)
print myTree
myDat, labels = createDataSet() # Because labels have been deleted in creat tree
print classify(myTree,labels,[0,0,0])
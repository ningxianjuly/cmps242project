# CMPS 242 Machine Learning project algothms implementation, Fall 2016 in UCSC
<p>
These are the implementations of several classfication algorithms in the Machine Learning course of UCSC.
</p>
<p>
word_dictionary_lr.py: The word dictionary generation python file for logistic regression.   
</p>
<p>
word_dictionary.py: The word dictionary generation python file for naive bayes.  
</p>
preprocess_yelp_dataset.py: Generate the training dataset and test dataset.  
</p>
<p>
naive_bayes.py: Naive bayes classification python file and get the classification accuracy of training dataset and test dataset.  
</p>
<p>
tfidf_feature.py: The features to generate tf * idf feature which you can use in Perception and Decision tree algorithms.   
</p>
<p>
<b>Perception:</b>
</p>
<p>
1. Run the preprocess_yelp_dataset.py to generate the training dataset and test dataset. 
</p>
<p>
2. Run the word_dictionary.py to generate positive words dictionary and negtive words dictionary.
</p>
<p>
3. Run the perception_modified.py to get the classication accuracy of training dataset and test dataset. The performances of them are as following:
</p>
<p>
We can not get the linear hyperplane to separate these points so these points can not classified by a linear hyperplane.
</p>
<p>
<b>Naive Bayes:</b>
</p>
<p>
1. Run the preprocess_yelp_dataset.py to generate the training dataset and test dataset. 
</p>
<p>
2. Run the word_dictionary.py to generate positive words dictionary and negtive words dictionary.
</p>
<p>
3. Run the naive_bayes.py to get the classication accuracy of training dataset and test dataset. The performances of them are as following:
</p>
<p>
Accuracy of training set: 0.8086 (1383732/1711225)
</p>
<p>
Accuracy of test set: 0.7802 (333789/427807)
</p>
<p>
<b>Decision Tree:</b>
</p>
<p>
1. Run the preprocess_yelp_dataset.py to generate the training dataset and test dataset. 
</p>
<p>
2.Run the word_dictionary_lr.py to generate feature dictionary.
</p>
<p>
3.Run the decision_tree_modified.py to train the decision tree and use the tree to get the classication accuracy of test dataset.The proformance of the decision tree is as following:                    
</p>
<p>
Accuracy of train set: 0.8389(1435583/1711225)
</p>
<p>
Accuracy of test set: 0.8687(371663/427807)
</p>
<p>
The decision feature we used :['great', 'good', 'like', 'just', 'get', 'food', 'one', 'place']
</p>
<p>
<b>KNN:</b>
</p>
<p>
1. Run the preprocess_yelp_dataset.py to generate the training dataset and test dataset. 
</p>
<p>
2.Run the word_dictionary_lr.py to generate feature dictionary.
</p>
<p>
3.Run the KNN.py to train the decision tree and use the tree to get the classication accuracy of test dataset.The proformance of the decision tree is as following:                    
</p>
<p>
Accuracy of train set: 0.8348(33392/40000)
</p>
<p>
Accuracy of test set: 0.8448(8448/10000)
</p>
<p>
The decision feature we used :['a', 'and', 'the', 'i', 'to']
</p>
<b>Logistic Regression:</b>
</p>
<p>
1. Run the preprocess_yelp_dataset.py to generate the training dataset and test dataset. 
</p>
<p>
2.Run the word_dictionary_lr.py to generate feature dictionary.
</p>
<p>
3.Run the logisticregressio.py to train the decision tree and use the tree to get the classication accuracy of test dataset.The proformance of the decision tree is as following:                    
</p>
<p>
Accuracy of train set: 0.839350308198(1436317/1711225)
</p>
<p>
Accuracy of test set: 0.86914090646(371894/427807)
</p>
<p>
The decision feature we used :['great', 'good', 'like', 'just', 'get', 'food', 'one', 'place']
</p>


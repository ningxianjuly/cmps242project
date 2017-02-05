'''
Created on Feb 4, 2017

@author: Tianyi Luo
'''
import logging, gensim
from gensim import corpora
from gensim import models, similarities
import os

def lda_topic_model(lda_topic_model_name, lda_num_topics, lda_num_top_words, lda_temp_model):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    loaded_lda_topics_model = lda_temp_model.load(lda_topic_model_name)
    loaded_lda_topics_model.print_topics(num_topics=lda_num_topics, num_words=lda_num_top_words)

def biterm_topic_model(biterm_topic_model_name, biterm_num_topics, biterm_num_top_words):
    print "Model biterm_topic_model!!!"

def get_lda_models():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    input_file = "nostem_processed_normal_format_Homework2_data.csv"
    documents_list = []
    for line in open(input_file, "r"):
        documents_list.append(line)
    texts = [[word for word in document.lower().split(" ")] for document in documents_list]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('temp_twitter.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize('temp_twitter_lda.mm', corpus)
    print "Generate the dictionary and lda corpus"
    
    if (os.path.exists("temp_twitter.dict")):
        dictionary = corpora.Dictionary.load('temp_twitter.dict')
        corpus = corpora.BleiCorpus('temp_twitter_lda.mm')
        print("Used files generated from first tutorial")
        
    #tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
    #corpus_tfidf = tfidf[corpus]
    
    #get the lda model
    lda_3_topics = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3)
    lda_4_topics = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=4)
    lda_5_topics = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
    #lda.print_topics(num_topics=5, num_words=10)
    lda_3_topics.save("lda_3_topics_model")
    lda_4_topics.save("lda_4_topics_model")
    lda_5_topics.save("lda_5_topics_model")
    
def get_biterm_models():
    print "Model 2!!!"

if __name__ == '__main__':
    ########################
    ##LDA from Genism
    ########################
    #get_lda_models()
    corpus = ""
    dictionary = ""
    if (os.path.exists("temp_twitter.dict")):
        dictionary = corpora.Dictionary.load('temp_twitter.dict')
        corpus = corpora.BleiCorpus('temp_twitter_lda.mm')
        print("Used files generated from first tutorial")
    
    lda_temp_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    model_name = "lda_3_topics_model"
    num_topics = 3
    num_words = 20
    print "LDA from Gensim (3 topics) top" + str(num_words)
    lda_topic_model(model_name, num_topics, num_words, lda_temp_model)
    
    
    model_name = "lda_4_topics_model"
    num_topics = 4
    num_words = 20
    print "LDA from Gensim (4 topics) top" + str(num_words)
    lda_topic_model(model_name, num_topics, num_words, lda_temp_model)
    
    model_name = "lda_5_topics_model"
    num_topics = 5
    num_words = 20
    print "LDA from Gensim (5 topics) top" + str(num_words)
    lda_topic_model(model_name, num_topics, num_words, lda_temp_model)
    
    ########################
    ##Biterm Topic Model
    ########################
    
    
    
    

    
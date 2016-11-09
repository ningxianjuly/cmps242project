# encoding=utf8 
import json
import os
import sys  
reload(sys)  
sys.setdefaultencoding('ISO-8859-1')
if __name__ == '__main__':
    dataset_file_location = '/Users/luotianyi/Desktop/CMPS242/hw3/'\
    'data_unzip/'
    stopwords_file = '/Users/luotianyi/Desktop/Develope/workspace/cmps242project'\
    '/google_stopwords'
    f_write_dataset_train = open('/Users/luotianyi/Desktop/CMPS242/'\
    'traindata_hw3_20161103', 'w')
    f_write_dataset_test = open('/Users/luotianyi/Desktop/CMPS242/'\
    'testdata_hw3_20161103', 'w')
    #print dataset_file_location
    line_num_int = 0
    line_valid_data = 0
    stop_words_list = []
    for temp_word in open(stopwords_file, 'r'):
        stop_words_list.append(str(temp_word.replace("\n","")))
    
    
    
    list_dirs = os.walk(dataset_file_location) 
    for root, dirs, files in list_dirs: 
        for d in dirs:
            ##############process the ham     
            temp_ham_file = dataset_file_location + d + "/ham/"
            list_dirs_ham = os.walk(temp_ham_file)
            for root_ham, dirs_ham, files_ham in list_dirs_ham: 
                num_ham = 0
                temp_train_num = len(files_ham) * 0.8
                print len(files_ham)
                for f in files_ham:
                    num_ham += 1
                    temp_text = ""
                    temp_file_location = temp_ham_file + f
                    if num_ham < temp_train_num:
                        #temp_num_file = 0
                        for temp_line in open(temp_file_location, 'r'):
                            #temp_num_file += 1 
                            temp_text += temp_line.replace("\r\n","") + " "
                        temp_result_str = '1' + '\t' + temp_text + '\n'
                        f_write_dataset_train.write(temp_result_str.encode('ISO-8859-1'))
                    else:
                        for temp_line in open(temp_file_location, 'r'):
                            #temp_num_file += 1 
                            temp_text += temp_line.replace("\r\n","") + " "
                        temp_result_str = '1' + '\t' + temp_text + '\n'
                        f_write_dataset_test.write(temp_result_str.encode('ISO-8859-1'))
                    #print f
            ##############process the spam
            temp_spam_file = dataset_file_location + d + "/spam/"
            list_dirs_spam = os.walk(temp_spam_file)
            for root_spam, dirs_spam, files_spam in list_dirs_spam:
                num_spam = 0
                temp_train_num = len(files_spam) * 0.8
                for f in files_spam:
                    num_spam += 1
                    temp_text = ""
                    temp_file_location = temp_spam_file + f
                    if num_spam < temp_train_num:
                        #temp_num_file = 0
                        for temp_line in open(temp_file_location, 'r'):
                            #temp_num_file += 1 
                            temp_text += temp_line.replace("\r\n","") + " "
                        temp_result_str = '0' + '\t' + temp_text + '\n'
                        f_write_dataset_train.write(unicode(temp_result_str).encode("ISO-8859-1"))
                    else:
                        for temp_line in open(temp_file_location, 'r'):
                            #temp_num_file += 1 
                            temp_text += temp_line.replace("\r\n","") + " "
                        temp_result_str = '0' + '\t' + temp_text + '\n'
                        f_write_dataset_test.write(unicode(temp_result_str).encode("ISO-8859-1"))
                    #print f   

import json
import os
import sys

reload(sys)
sys.setdefaultencoding('ISO-8859-1')
if __name__ == '__main__':
    dataset_file_location = '/Users/Tansy/Desktop/CMPS242/HWK3/' \
                            'traindata/'
    datatestset_file_location = '/Users/Tansy/Desktop/CMPS242/HWK3/' \
                            'testdata/'
    stopwords_file = '/Users/Tansy/Desktop/CMPS242/project' \
                     '/google_stopwords'
    f_write_dataset_train = open('/Users/Tansy/Desktop/CMPS242/HWK3/' \
                                 'traindata_hw3', 'w')
    f_write_dataset_test = open('/Users/Tansy/Desktop/CMPS242/HWK3/' \
                                'testdata_hw3', 'w')
    # print dataset_file_location
    line_num_int = 0
    line_valid_data = 0
    stop_words_list = []
    for temp_word in open(stopwords_file, 'r'):
        stop_words_list.append(str(temp_word.replace("\n", "")))
    ##############process the training data set
    list_dirs = os.walk(dataset_file_location)
    for root, dirs, files in list_dirs:
        for d in dirs:
            ##############process the ham
            temp_ham_file = dataset_file_location + d + "/ham/"
            list_dirs_ham = os.walk(temp_ham_file)
            for root_ham, dirs_ham, files_ham in list_dirs_ham:
                num_ham = 0
                for f in files_ham:
                    num_ham += 1
                    temp_text = ""
                    temp_file_location = temp_ham_file + f
                    for temp_line in open(temp_file_location, 'r'):
                        # temp_num_file += 1
                        temp_text += temp_line.replace("\r\n", "") + " "
                    temp_result_str = '1' + '\t' + temp_text + '\n'
                    f_write_dataset_train.write(temp_result_str.encode('UTF-8'))
                print num_ham

            temp_spam_file = dataset_file_location + d + "/spam/"
            list_dirs_spam = os.walk(temp_spam_file)
            for root_spam, dirs_spam, files_spam in list_dirs_spam:
                num_spam = 0
                for f in files_spam:
                    num_spam += 1
                    temp_text = ""
                    temp_file_location = temp_spam_file + f
                    # temp_num_file = 0
                    for temp_line in open(temp_file_location, 'r'):
                        # temp_num_file += 1
                        temp_text += temp_line.replace("\r\n", "") + " "
                    temp_result_str = '0' + '\t' + temp_text + '\n'
                    f_write_dataset_train.write(unicode(temp_result_str).encode("UTF-8"))
                print num_spam

    ##############process the test data set
    list_dirs = os.walk(datatestset_file_location)
    for root, dirs, files in list_dirs:
        for d in dirs:
            ##############process the ham
            temp_ham_file = datatestset_file_location + d + "/ham/"
            list_dirs_ham = os.walk(temp_ham_file)
            for root_ham, dirs_ham, files_ham in list_dirs_ham:
                num_ham = 0
                for f in files_ham:
                    num_ham += 1
                    temp_text = ""
                    temp_file_location = temp_ham_file + f
                    for temp_line in open(temp_file_location, 'r'):
                        # temp_num_file += 1
                        temp_text += temp_line.replace("\r\n", "") + " "
                    temp_result_str = '1' + '\t' + temp_text + '\n'
                    f_write_dataset_test.write(temp_result_str.encode('UTF-8'))

                print num_ham

            temp_spam_file = datatestset_file_location + d + "/spam/"
            list_dirs_spam = os.walk(temp_spam_file)
            for root_spam, dirs_spam, files_spam in list_dirs_spam:
                num_spam = 0
                for f in files_spam:
                    num_spam += 1
                    temp_text = ""
                    temp_file_location = temp_spam_file + f
                    # temp_num_file = 0
                    for temp_line in open(temp_file_location, 'r'):
                        # temp_num_file += 1
                        temp_text += temp_line.replace("\r\n", "") + " "
                    temp_result_str = '0' + '\t' + temp_text + '\n'
                    f_write_dataset_test.write(unicode(temp_result_str).encode("UTF-8"))
                print num_spam



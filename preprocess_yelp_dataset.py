import json

if __name__ == '__main__':
    dataset_file_location = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
    stopwords_file = '/Users/luotianyi/Desktop/Develope/workspace/cmps242project'\
    '/google_stopwords'
    f_write_dataset_train = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'traindata_20161103', 'w')
    f_write_dataset_test = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'testdata_20161103', 'w')
    #print dataset_file_location
    line_num_int = 0
    line_valid_data = 0
    stop_words_list = []
    for temp_word in open(stopwords_file, 'r'):
        stop_words_list.append(str(temp_word.replace("\n","")))
    
    for line in open(dataset_file_location, 'r'):
        line_num_int += 1
        if line_num_int % 5000 == 0:
            print str(line_num_int) + " lines are handled"      
        if line_valid_data == 50000:
            break
        temp_result_str = ''
        #print line
        data = json.loads(line)
        #print data['text']
        #print data['stars']
        text_lower_string = data['text'].lower()
        rating_int = int(data['stars'])
        if rating_int == 4 or rating_int == 5:
            line_valid_data += 1
            #temp_result_str = '1' + '\t' + text_lower_string.replace("\n","") + '\n'
            temp_stopwords_list = text_lower_string.replace("\n","").split(" ")
            temp_string = ""
            temp_index = 0
            for temp_word in temp_stopwords_list:
                temp_index += 1
                if temp_index == len(temp_stopwords_list):
                    if temp_word not in stop_words_list:
                        temp_string += temp_word + "\n"
                else: 
                    if temp_word not in stop_words_list:
                        temp_string += temp_word + " "
            temp_result_str = '1' + '\t' + temp_string
            if line_valid_data <= 1711125:
                f_write_dataset_train.write(temp_result_str.encode('utf-8'))
            else:
                f_write_dataset_test.write(temp_result_str.encode('utf-8'))
        if rating_int == 0 or rating_int == 1:
            line_valid_data += 1
            temp_result_str = '0' + '\t' +text_lower_string.replace("\n","") + '\n'
            temp_stopwords_list = text_lower_string.replace("\n","").split(" ")
            temp_string = ""
            temp_index = 0
            for temp_word in temp_stopwords_list:
                temp_index += 1
                if temp_index == len(temp_stopwords_list):
                    if temp_word not in stop_words_list:
                        temp_string += temp_word + "\n"
                else: 
                    if temp_word not in stop_words_list:
                        temp_string += temp_word + " "
            temp_result_str = '1' + '\t' + temp_string
            if line_valid_data <= 1711125:
                f_write_dataset_train.write(temp_result_str.encode('utf-8'))
            else:
                f_write_dataset_test.write(temp_result_str.encode('utf-8'))

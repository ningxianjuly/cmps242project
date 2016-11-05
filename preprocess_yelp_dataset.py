import json

if __name__ == '__main__':
    dataset_file_location = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
    f_write_dataset_train = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'traindata_20161103', 'w')
    f_write_dataset_test = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'testdata_20161103', 'w')
    #print dataset_file_location
    line_num_int = 0
    line_valid_data = 0
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
            temp_result_str = '1' + '\t' +text_lower_string.replace("\n","") + '\n'
            if line_valid_data <= 40000:
                f_write_dataset_train.write(temp_result_str.encode('utf-8'))
            else:
                f_write_dataset_test.write(temp_result_str.encode('utf-8'))
        if rating_int == 0 or rating_int == 1:
            line_valid_data += 1
            temp_result_str = '0' + '\t' +text_lower_string.replace("\n","") + '\n'
            if line_valid_data <= 40000:
                f_write_dataset_train.write(temp_result_str.encode('utf-8'))
            else:
                f_write_dataset_test.write(temp_result_str.encode('utf-8'))
    
    
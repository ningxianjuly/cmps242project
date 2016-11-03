import json

if __name__ == '__main__':
    dataset_file_location = '/Users/luotianyi/Desktop/CMPS242/project/'\
    'yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
    f_write_dataset = open('/Users/luotianyi/Desktop/CMPS242/project/'\
    'trainingdata_20161102', 'w')
    #print dataset_file_location
    line_num_int = 0
    for line in open(dataset_file_location, 'r'):
        line_num_int += 1
        if line_num_int % 5000 == 0:
            print str(line_num_int) + " lines are handled"
        temp_result_str = ''
        #print line
        data = json.loads(line)
        #print data['text']
        #print data['stars']
        text_lower_string = data['text'].lower()
        rating_int = int(data['stars'])
        if rating_int == 4 or rating_int == 5:
            temp_result_str = '1' + '\t' +text_lower_string.replace("\n","") + '\n'
            f_write_dataset.write(temp_result_str.encode('utf-8'))
        if rating_int == 0 or rating_int == 1:
            temp_result_str = '0' + '\t' +text_lower_string.replace("\n","") + '\n'
            f_write_dataset.write(temp_result_str.encode('utf-8'))
    
    
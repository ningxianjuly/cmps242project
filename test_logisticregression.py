'''
Created on 30 Nov, 2016

@author: luotianyi
'''
  
import unittest  
import logisticregression
  
class mytest(unittest.TestCase):        
    def setUp(self):  
        pass  
 
    def tearDown(self):
        pass
  
    def test_sigmoid(self):  
        predict_result = logisticregression.cal_sigmoid([2,3], [1.0, 1.0])
        print predict_result
        true_result = 0.9933071490757153
        self.assertEqual(predict_result, true_result, "test sigmoid function fail")
                    
if __name__ =='__main__':  
    unittest.main()

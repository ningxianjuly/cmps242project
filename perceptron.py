'''
Perceptron Example 

Input X : [ X1, X2, Label ] ~ Two featuers followed by label
Output Y = { -1 , 1 }
Y = sign ( W * X + b )

@author: Chengye Tang
'''
import time
import matplotlib.pyplot as plt

""" initialize parameters """
W = [1, 1]
b = 0
learning_rate = 0.05

""" Given input X, compute output """
def predict_result (X):
    y = W[0] * X[0] + W[1] * X[1] + b
    if y > 0 :
        return 1;
    else :
        return -1;


def update_parameter(X, y, label):
    ''' 
    If predicted y equals label 
    no need to update parameter
    '''
    global b
    if y == label :
        return
    else :
        W[0] = W[0] + learning_rate * label * X[0]
        W[1] = W[1] + learning_rate * label * X[1]
        b = b + learning_rate * label
    

def train (data):
    ''' iterate at most 100 times '''
    global b
    
    for i in range (1, 100) : 
        error = 0.0
        for num in data : 
            X = num[0:2]
            label = num[2]
            y = predict_result(X)
            
      
            if label != y :
                error +=  1
                update_parameter(X, y, label)
            
            
        draw(data, i)
            
        if error == 0 :
            break;

    



def draw(data, i):
    global b
    print '{} * X1 + {} * X2 + {}'.format(W[0], W[1], b) 
    
    figs = plt.figure(i)
    plt.plot([0,1,1,2], [0,0,1,1], 'ro')
    plt.plot([0,0,1,1], [4,6,8,9], 'bo')
    
    px1 = -1
    py1 = (-1 * W[0] / W[1]) * float(px1) - b / W[1]
    px2 = 10
    py2 = (-1 * W[0] / W[1]) * float(px2) - b / W[1]
    #print '[{},{}]  [{},{}]'.format(px1, py1, px2, py2) 
    print ''
    
    plt.plot([px1, px2], [py1 , py2], color = 'black')
    plt.axis([-1, 10, -1, 10])
    figs.show()
    time.sleep(1)
    

if __name__ == '__main__':
    input_data = [
        [0, 0, -1],
        [1, 0, -1],
        [1, 1, -1],
        [2, 1, -1],
        [4, 4, 1],
        [4, 6, 1],
        [6, 8 , 1],
        [1, 10, 1]
    ]
    
    train(input_data)
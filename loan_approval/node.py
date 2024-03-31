class Node:
    '''
    This is a class which is used for creating decision tree.
    This class is considered as the single tree node in decision tree.
    ....
    
    Attributes:
    -----------
    feature:
        Feature that is splitted.
    thresh:
        Threshold for the split.
    left:
        Data at the Left child of given node.
    right:
        Data at the Right child of given node.
    information_gain:
        Information Gain of the given node.
    value:
        Current value of the given node.
    
    Methods:
    ---------
    __init__(params)
        Constructor of the Node class
    print_attributes(self):
        Prints the attributes of the class.
        
    '''
    def __init__(self, feature = None, thresh=None, left=None, right=None, information_gain=None,value=None):
        '''
        This is the constructor code of the Node class.
        ......
        
        Parameters
        -----------
        
        feat:
        thresh:
        left:
        right:
        information_gain:
        value:
        '''
        self.feature = feature
        self.thresh = thresh
        self.left = left
        self.right = right
        self.information_gain = information_gain
        self.value = value
    
    def print_attributes(self):
        '''
        This is the method for printing the attributes of the given node.
        '''
        print("Feature to be split:"+(self.feature))
        print("Threshold of split:"+(self.thresh))
        print("Left child:"+(self.left))
        print("Right child:"+(self.right))
        print("Information Gain:"+(self.information_gain))
        print("Value at current node:"+(self.value))
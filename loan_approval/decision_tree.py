from collections import Counter
from .node import Node
import numpy as np

class DecisionTree:
    '''
    This class implements the decision tree classifier with the help of Node class.
    ...
    Basic algorithm:
    ----------------    
        Step 1: CREATE A ROOT NODE.
        Step 2: Find the best attribute to split the dataset using impurity metrics.
            Step 2.1: Calculate Overall entropy of the dataset output column. h_y(S)
            Step 2.2: For all feature columns(X):
                Step 2.2.1: Calculate entropy of given column(x_i) 
                    with different sets of value i.e. h_x_i^{value}(S)
                Step 2.2.2: Calculate information gain of given column 
                    through the help of entropy i.e. ig_x_i
            Step 2.3: Compare information gains of all columns
            Step 2.4: Select Maximum information gain column as best split.
            
        Step 3: Divide given dataset(S) with the selected column as the split.
        Step 4: Create the child nodes to the root node based on the split.
        Step 5: Repeat Step 2-Step 4 recursively, until leaf nodes are found. 
        (leaf node: the node with no child).
    ...
    Attributes:
    -----------
        minimum_samples_to_split: int
            Minimum number of splits to be done while splitting.
        max_depth: int
            Maximum depth of the tree. 
            (depth of tree: number of columns that are splitted.)
    ....
    Methods:
        __init__():
            Constructor for initializing the decision tree.
        _entropy(): protected method, static method
            calculates entropy of the given column in dataset "s".
        _information_gain(): protected method
            calculates information gain of the given column in dataset "s".
        _calculate_best_split():protected method
            selects the best split based on the given entropy and information.
            Calculates threshold, right child, left child, etc.
        _build(): protected method
            Builds the decision tree.
        fit():
            trains the decision tree with basic algorithm (shown above).
        _predict(): protected method
            helper function for traversing the decision tree.
        predict()
            predicts the output.
    '''
    def __init__(self, list_features, minimum_samples_to_split=2, max_depth=5):
        '''
        This is the constructor for Decision Tree class.
        It initializes the Decision Tree.
        ...
        Parameters:
            minimum_samples_to_split: int
                Minimum samples required for splitting the node.
            max_depth: int
                Total depth of split of decision tree.
        '''
        self.minimum_samples_to_split = minimum_samples_to_split
        self.max_depth = max_depth
        self.list_features = list_features
        # self.predict_level_check = 0
        
    @staticmethod
    def _entropy(data):
        '''
        Entropy is a impurity metric that measures the disorder.
        
        Formula for entropy:
            H_column = - sum_{i=1}^{n}(p_i*log_2(p_i))
        ...
        Parameters:
            data: list
        ...
        returns:
            entropy: in floating point value
        '''
        # calculating total count of the given values.
        count = np.bincount(np.array(data, dtype=np.int64))
        # probabilities of the all value in the class label
        prob = count/len(data)
        # initializing entropy
        entropy = 0
        # calculating entropy for all values
        for i in prob:
            if i>0:
                entropy += i * np.log2(i)
        return -(entropy)
    
    def _information_gain(self,parent_node, left_child_node, right_child_node):
        '''
        This function calculates information gain for the current node.
        Information gain can be calculated by:
            IG = Entropy(Parent) - Sum(Entropy(child)*Probabilities_of_child_occurence)
        ...
        Parameters:
            parent_node: List
                Parent node of the current node.
            left_child_node: List
                Left child node of the current node.
            right_child_node: List
                Right child node of the current node.
        ...
        Returns:
            Information gain in the current node. 
        '''
        # Calculating number of probabilities of left and right child
        left_childs = len(left_child_node)/len(parent_node)
        right_childs = len(right_child_node)/len(parent_node)
        # Calculating entropy for left, right and parent node
        parent_entropy = self._entropy(parent_node)
        left_entropy = self._entropy(left_child_node)
        right_entropy = self._entropy(right_child_node)
        # Based on previous calculation, calculation of information gain
        information_gain = parent_entropy -((left_entropy*left_childs)+(right_childs)*right_entropy)
        return information_gain
    
    def _calculate_best_split(self,features,label):
        '''
        This function calculates the best split based in information gain 
        calculated for X and y.
        ...
        Parameters:
        ----------
            features: numpy array
                Input features for the model
            label: numpy array
                Output label of the model
        ...
        Returns:
        --------
            best_split: dict
                Best split has columns, threshold of the split, left childs, right childs,
                information gain value.
        '''
        # Initializing the values
        best_split = {}
        best_information_gain = -1
        (_,columns) = features.shape
        # print(columns)
        # Calculating best split
        for i in range(columns):
            # Selecting specific input feature column.
            x_current = features[:,i]
            for threshold in np.unique(x_current):
                # Creating  dataset by concatenating X and y.
                dataset = np.concatenate((features, label.reshape(1, -1).T), axis=1)
                # Splitting dataset into two halfs (left and right) based on rows.
                dataset_left = np.array([row for row in dataset if row[i] <= threshold])
                dataset_right = np.array([row for row in dataset if row[i] > threshold])
                # Selecting the best information gain.
                if (len(dataset_left) > 0 ) and (len(dataset_right) > 0):
                    y = dataset[:,-1]
                    y_left = dataset_left[:,-1]
                    y_right = dataset_right[:,-1]
                    # Calculating information gain.
                    information_gain = self._information_gain(y,y_left,y_right)
                    if (information_gain > best_information_gain):
                        best_split = {
                                "feature_index":i,
                                "threshold":threshold,
                                "left":dataset_left,
                                "right":dataset_right,
                                "information_gain":information_gain
                            }
                        best_information_gain = information_gain
        # print("Column Split:{0}".format(best_split["feature_index"]))
        print("Splitted_column Name:{0}".format(self.list_features[best_split['feature_index']]))
        return best_split
    
    def _build_tree(self, X,y, depth =0):
        """
        This function builds the tree data structure based on the based split of the data.
        This method uses recursion such that the all nodes until leaf node or certain depth is built.
        ...
        Parameters:
        ----------
            X: numpy array
                Input features for the model
            y: numpy array
                Output label of the model
            depth:int
                Current depth of the tree used as stopping criteria.
        ...
        Returns:
        --------
            Node: Object
                Node in the form of the built tree.
        """
        num_rows, num_cols = X.shape
        print("--------------------------------------------------")
        print("At Level {0}:".format(depth))
        print("Number of instances of X: {0}".format(num_rows))
        print("Number of columns to split in X: {0}".format(num_cols))
        print("--------------------------------------------------")
        # condition 1 checks whether there is number of rows less than minimum samples to split.
        condition_1 = (num_rows >=self.minimum_samples_to_split)
        # condition 2 checks whether the current depth is less than or equal to max depth defined by the user.
        condition_2 = (depth<=self.max_depth)
        # checking both condition to build the tree.
        if condition_1 and condition_2:
            # Selecting the best split of the current depth.
            splitted_data = self._calculate_best_split(X, y)
            # Checking whether the best split given by the data is pure or not.
            if splitted_data['information_gain'] > 0:
                # Using recursion for getting left and right child to the current depth of the tree.
                # Left child split
                new_depth = depth+1
                print("Left Split to level:{0}".format(new_depth))
                X_left = splitted_data['left'][:,:-1]
                y_left = splitted_data['left'][:,-1]
                left_child = self._build_tree(X_left, y_left, new_depth)
                # right child split
                print("Right Split to level:{0}".format(new_depth))
                X_right = splitted_data['right'][:,:-1]
                y_right = splitted_data['right'][:,-1]
                right_child = self._build_tree(X_right, y_right, new_depth)
                # After calculating returning the data to the previous itreation of recursion.
                return node.Node(
                    feature= splitted_data['feature_index'],
                    thresh= splitted_data['threshold'],
                    left = left_child,
                    right = right_child,
                    information_gain = splitted_data['information_gain']
                )
        # Returning the most common target value for the leaf node.
        return node.Node(value= Counter(y).most_common(1)[0][0])
    
    def train_model(self,X,y):
        """
        This method is used for training the model.
        ...
        Parameters:
        ----------
            X: numpy array
                Input features for the model
            y: numpy array
                Output label of the model
        ...
        Returns:
        --------
            None (Only training of the model occurs.)
        """
        print("--------------------------------------------------")
        print("Training Process Started.")
        self.root = self._build_tree(X, y)
    
    def _predict(self,x,tree):
        """
        This method is a helper function to predict the data.
        ...
        Parameters:
        ----------
            x: numpy array
                Input features for the model to be tested.
            tree: Node
                Built tree.
        ...
        Returns:
        --------
            Predicted_class: float
        """
        if tree.value != None:
            return tree.value
        feature = x[tree.feature]
        # print("Tree Feature :{0}".format(tree.feature))
        # go to left
        if feature <= tree.thresh:
            # self.predict_level_check+=1
            print("Left Split:{0}<={1} ".format(self.list_features[tree.feature], tree.thresh))
            return self._predict(x=x, tree = tree.left)
        if feature > tree.thresh:
            # self.predict_level_check+=1
            print("Right Split:{0}>{1} ".format(self.list_features[tree.feature], tree.thresh))
            return self._predict(x=x, tree=tree.right)
        
    def predict(self, X, list_features):
        """
        This method predicts the output label of the given data.
        ...
        Parameters:
        ----------
            x: numpy array
                Input features for the model to be tested.
        ...
        """
        self.list_features=list_features
        return [self._predict(x, self.root) for x in X]
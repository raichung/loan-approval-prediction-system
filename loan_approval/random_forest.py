import numpy as np
from collections import Counter
from .decision_tree import DecisionTree

class RandomForest:
    """
    This class implements random forest (ensemble of decision tree.)
    ...
    Basic Idea:
    ....
    Attributes:
        num_trees: int
            Number of trees used in the random forest model
        minimum_samples_to_split: int
            Minimum number of splits to be done while splitting.
        max_depth: int
            Maximum depth of the tree. 
            (depth of tree: number of columns that are splitted.)
    ....
    Methods:
        __init__():
            Constructor for creating the random forest model.
        __sample():
            Static method for generating bootstrap samples.
        train_model():
            Trains the random forest algorithm
        predict():
            Predicts the output labels with the help of data.
    """
    def __init__(self,list_features,num_trees, minimum_samples_to_split=2,max_depth=5):
        """
        This is the constructor which assigns the value to the given attributes.
        ....
        Paramaters:
            num_trees:  int
                Number of decision trees in the random forest model.
            minimum_samples_to_split: int
                Minimum number of splits to be done while splitting.
            max_depth: int
                Maximum depth of the tree. 
                (depth of tree: number of columns that are splitted.)
        """
        self.num_trees = num_trees
        self.minimum_samples_to_split = minimum_samples_to_split
        self.max_depth = max_depth
        self.trees = []
        self.list_features = list_features
    
    @staticmethod
    def __sample(X,y):
        """
        This is a helper function for bootstrap sampling of the data.
        ....
        Parameters:
            X: numpy.array
                Features of the dataset.
            y: numpy.array
                Output labels of the dataset.
        ....
        Returns:
            (samples_x, samples_y): tuple
                Randomly generated samples for bootstrapping.
        """
        n_rows, n_cols = X.shape
        # Sampling the dataset with replacements
        sample = np.random.choice(a=n_rows,size=n_rows, replace=True)
        samples_x = X[sample]
        samples_y = y[sample]
        return samples_x, samples_y
    
    def train_model(self,X,y):
        """
        This method trains the random forest model with the help of input 
        features and output labels.
        ....
        Parameters:
            X: numpy.array
                Input features of the dataset
            y: numpy.array
                Output labels of the dataset.
        """
        i = 0
        if len(self.trees)>0:
            self.trees = []
        tree_built = 0
        while tree_built < self.num_trees:
            # try:
            print("--------------------------------------------------")
            print("Itreation: {0}".format(i))
            tree = decision_tree.DecisionTree(
                    list_features=self.list_features,
                    minimum_samples_to_split= self.minimum_samples_to_split,
                    max_depth= self.max_depth
                )
            sample_x, sample_y = self.__sample(X, y)
            tree.train_model(sample_x, sample_y)
            self.trees.append(tree)
            tree_built+=1
            i+=1
            # except Exception as e:
            #     print(e)
            #     continue
    
    def predict(self,X, list_features):
        """
        This method predicts the output label with the ensemble 
        of decision trees previously trained.
        ....
        Parameters:
            X: numpy.array
                Input features for predicting the output labels.
        """
        self.list_features = list_features
        labels = []
        counter= 0
        for tree in self.trees:
            counter+=1
            print("-----------------------------")
            print("Tree:{0}".format(counter))
            labels.append(tree.predict(X,list_features))
        labels = np.swapaxes(a=labels, axis1=0, axis2=1)
        predictions = []
        for preds in labels:
            counter = Counter(preds)
            predictions.append(counter.most_common(1)[0][0])
        return predictions
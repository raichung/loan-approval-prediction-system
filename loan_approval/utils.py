import pandas as pd
import pickle
from django.conf import settings
import os
import joblib
import sys
from loan_approval import decision_tree, node, random_forest

class Model:
    ohe_pipeline = None
    ohe_features  = None
    numerical_pipeline = None
    dtree_pipeline = None
    rf_pipeline =  None
    numeric_features = ['person_age', 'person_income', 'person_emp_length', 'loan_amnt', 'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length']
    binary_features = ['cb_person_default_on_file']
    categorical_features = ['person_home_ownership', 'loan_intent', 'loan_grade']
    def __init__(self, person_age, person_income, home_ownership,
                 employment_length,intent,grade,amount,interest_rate, 
                 percent_to_income,default_on_file,credit_history_length):
        # Set Values
        self.person_age = person_age
        self.person_income = person_income
        self.home_ownership = home_ownership
        self.employment_length = employment_length
        self.intent = intent
        self.grade = grade
        self.amount = amount
        self.interest_rate = interest_rate
        self.percent_to_income = percent_to_income
        self.default_on_file =self.process_booleans(default_on_file)
        self.credit_history_length = credit_history_length
    
    def open_files(self,file_name):
        file_path = os.path.join(settings.BASE_DIR, "loan_approval/"+file_name)
        with open(file_path,"rb") as file:
            obj = pickle.load(file)
        return obj
    
    def load_file(self,file_name):
        sys.modules['decision_tree'] = decision_tree
        sys.modules['node'] = node
        sys.modules['random_forest'] = random_forest
        # sys.modules['']
        file_path = os.path.join(settings.BASE_DIR, "loan_approval/"+file_name)
        with open(file_path,"rb") as file:
            obj = joblib.load(file)
        return obj

    def create_dataframe(self):
        #         details = {'person_age': {0: 22},
        #  'person_income': {0: 59000},
        #  'person_home_ownership': {0: 'RENT'},
        #  'person_emp_length': {0: 123.0},
        #  'loan_intent': {0: 'PERSONAL'},
        #  'loan_grade': {0: 'D'},
        #  'loan_amnt': {0: 35000},
        #  'loan_int_rate': {0: 16.02},
        #  'loan_percent_income': {0: 0.59},
        #  'cb_person_default_on_file': {0: 'Y'},
        #  'cb_person_cred_hist_length': {0: 3}}
        details =  {'person_age': {0: self.person_age},
                    'person_income': {0: self.person_income},
                    'person_home_ownership': {0: self.home_ownership},
                    'person_emp_length': {0: self.employment_length},
                    'loan_intent': {0: self.intent},
                    'loan_grade': {0: self.grade},
                    'loan_amnt': {0: self.amount},
                    'loan_int_rate': {0: self.interest_rate},
                    'loan_percent_income': {0: self.percent_to_income},
                    'cb_person_default_on_file': {0: self.default_on_file},
                    'cb_person_cred_hist_length': {0: self.credit_history_length}
                    }
        self.df = pd.DataFrame(details)
        return self.df
    
        
    def process_booleans(self,boolean):
        # print("Hello")
        # print(type(boolean))
        if boolean == True:
            return 1
        elif boolean == False:
            return 0
    
    def preprocess_data(self,dataframe):
        
        
        for columns in dataframe.columns:
            dataframe[columns] = dataframe[columns].astype(str)
            if columns == "cb_person_default_on_file":
                dataframe[columns] = 'Y'
            print(" ")
            print(dataframe[columns])
            print(" ")

        print("data frame is: ")
        print(dataframe)
        
        self.numerical_pipeline = self.load_file("pickle_files/one_hot_encoder.pkl")
        X = dataframe.copy(deep = True)

        print(" info is : ")
        print(X.info())



        X.to_csv('details_in.csv', index=False)
        categorical_columns = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        new_X = self.numerical_pipeline.transform(dataframe[categorical_columns])
        print(new_X)
        return new_X
        
        
    
    def predict_data(self):
        self.df = self.create_dataframe()
        X = self.preprocess_data(self.df)
        self.dtree_pipeline = self.open_files("pickle_files/dtree.pkl")
        self.rf_pipeline = self.load_file("pickle_files/random_forest_model.pkl")
        # print(self.ohe_features)
        prediction = self.rf_pipeline.predict(X)

        print("the  prediction is : ", prediction[0])
        if prediction[0] == 0:
            return False
        elif prediction[0] == 1:
            return True
        # return prediction
    


from django.contrib.auth.models import User
from loan_approval.models import Loan, LoanDetails, LoanPrediction
import pandas as pd
import os
from django.conf import settings
import logging
from .utils import Model
# users = User.objects.all()

class Loader:
    users = User.objects.all()
    employees = None
    applicants = None
    
    def __init__(self):
        logging.basicConfig(filename='population_script.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,  datefmt='%d-%b-%y %H:%M:%S')
        logging.info('Logger started.')
        # print(self.users)
        self.check_employee()
        self.check_applicants()
    
    def check_employee(self):
        self.employees = list()
        for i in range(len(self.users)):
            condition_1 = not self.users[i].is_superuser
            condition_2 = self.users[i].is_staff
            if condition_1 and condition_2:
                # print(self.users[i],condition_1,condition_2)
                self.employees.append(self.users[i])
        # print(self.employees)
    
    def check_applicants(self):
        self.applicants = list()
        for i in range(len(self.users)):
            condition_1 = not self.users[i].is_staff
            if condition_1:
                # print(self.users[i],condition_1)
                self.applicants.append(self.users[i])
        # print(self.applicants)
        
    def load_csv(self):
        file_name = "data/new_loans.csv"
        file_path = os.path.join(settings.BASE_DIR, "loan_approval/"+file_name)
        self.df = pd.read_csv(file_path)
        logging.info("Reading csv file from data column.")
        self.df = self.df.iloc[:1050]
        # print(self.df)
        # print(self.df.columns)
    
    def split_columns(self):
        self.employee_columns = ['cb_person_cred_hist_length','loan_int_rate',
                            'cb_person_default_on_file','loan_grade','loan_percent_income',]
        # self.employee_df = self.df[employee_columns]
        self.applicant_columns = ['person_home_ownership','person_emp_length','loan_amnt',
                             'loan_intent','person_age','person_income']
        # self.applicant_df = self.df[applicant_columns]
        # # print(self.employee_df)
        # print("Employe columns: {0}".format(self.employee_df.columns))
        # # print(self.applicant_df)
        # print("Applicant columns: {0}".format(self.applicant_df.columns))
        self.populate_data()
        # self.populate_data_single_instance(1, "ankit", "applicant")
    
    def populate_data(self):
        print("Database population")
        num_employees = len(self.employees)
        num_applicants = len(self.applicants)
        if num_employees == num_applicants:
            for i in range(num_employees):
                # populate_single_instance
                employee = self.employees[i].employee
                applicant = self.applicants[i].applicant
                logging.info("Itreation {0}:".format(i))
                logging.info("APPLICANT: {0}".format(applicant))
                logging.info("EMPLOYEE: {0}".format(employee))
                # print(employee, applicant)
                for j in range(250*i,250*(i+1)):
                    print(j)
                    logging.info("Data Instance: {0}".format((j+1)))
                    self.populate_data_single_instance((j+1),employee=employee, applicant=applicant)
    
    def populate_data_single_instance(self,index, employee, applicant):
        # try:
        # print(len(self.df))
        data_instance = self.df.loc[index]
        # print(data_instance)
        # logging.info(data_instance)
        loan = self.populate_loan( data_instance, applicant,employee)
        loan_status = False
        if loan:
            loan_status = self.populate_loan_details(data_instance, loan)
            if loan_status:
                self.create_prediction(loan)
            # pass
        
        # except:
            # logging.error("Data Instance: {0} FAILED to save completely.".format(index))
        
    
    def populate_loan(self,data,applicant, employee):
        age = data['person_age']
        home_ownership = data['person_home_ownership']
        emp_length = int(data['person_emp_length'])
        amount = data['loan_amnt']
        income = data['person_income']
        intent = data['loan_intent']
        logging.info("""PERSON AGE: {0},HOME OWNERSHIP: {1}, EMP LENGTH: {2}, AMOUNT: {3}, INCOME: {4}, INTENT: {5}""".format(age,home_ownership,
                                                                     emp_length,amount,
                                                                     income,intent))

        try:
            loan = Loan.objects.create(person_age=age,home_ownership=home_ownership,
                                   emp_length=emp_length,loan_amount=amount,
                                   income= income,loan_intent=intent,
                                   applicant_details=applicant,managed_by=employee)
            loan.save()
            return loan
        except:
            logging.error("Could not create a loan object.")
            return False
    
    def populate_loan_details(self,data,loan):
        credit_history = data['cb_person_cred_hist_length']
        credit_default = self.process_default(data['cb_person_default_on_file'])
        interest_rate = data['loan_int_rate']
        grade = data['loan_grade']
        loan_percent_to_income = data['loan_percent_income']
        logging.info(""" CREDIT HISTORY: {0}, CREDIT DEFAULT: {1}, INTEREST RATE: {2},GRADE: {3}, LOAN PERCENT TO INCOME : {4}""".format(credit_history,credit_default,interest_rate,
                                grade,loan_percent_to_income))
        # print(credit_history, credit_default,interest_rate,grade,loan_percent_to_income, loan)
        # print("Loan Details Object created.")
        try:
            loandetails = LoanDetails.objects.create(credit_history=credit_history, credit_default=credit_default,
                                                 interest_rate=interest_rate, grade=grade,
                                                 loan_percent_to_income=loan_percent_to_income, loan_request=loan)
            loandetails.save()
            return True
        except:
            logging.error("Could create a loan details object.")
            return False
    
    def process_default(self,default):
        if default == "Y":
            return True
        elif default=="N":
            return False
    
    def create_prediction(self, loan):
        prediction_status = True
        model = self.create_model(loan)
        loan_status = model.predict_data()
        logging.info("PREDICTION STATUS: {0}, LOAN STATUS: {1}".format(prediction_status, loan_status))
        try:
            prediction = LoanPrediction.objects.create(prediction_status=prediction_status, loan_status=loan_status, loan_data= loan)
            prediction.save()
        except:
            logging.error("Could not create loan prediction object.")
    
    def create_model(self,loan):
        person_age = loan.person_age
        income = loan.income
        intent = loan.loan_intent
        emp_length = loan.emp_length
        amount = loan.loan_amount
        ownership = loan.home_ownership
        credit_history = loan.loandetails.credit_history
        rate = loan.loandetails.interest_rate
        default = loan.loandetails.credit_default
        grade = loan.loandetails.grade
        percent_to_income = loan.loandetails.loan_percent_to_income
        print(person_age)
        model = Model(
            person_age = person_age,
            person_income = income,
            home_ownership = ownership,
            employment_length = emp_length,
            intent = intent,
            grade = grade,
            amount = amount,
            interest_rate = rate,
            percent_to_income = percent_to_income,
            default_on_file = default,
            credit_history_length = credit_history
        )
        return model

        
        


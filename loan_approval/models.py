from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Applicant(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.applicant.username}'
    

class Employee(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.employee.username}'
    
class Loan(models.Model):
    OWNERSHIP_CHOICES = [('RENT','RENT'),
                         ('OWN','OWN'),
                         ('MORTGAGE','MORTGAGE'),
                         ('OTHER','OTHER')
                         ]
    INTENTIONS = [('PERSONAL','PERSONAL'),
                  ('EDUCATION','EDUCATION'),
                  ('MEDICAL','MEDICAL'),
                  ('VENTURE','VENTURE'),
                  ('HOMEIMPROVEMENT','HOMEIMPROVEMENT'),
                  ('DEBTCONSOLIDATION','DEBTCONSOLIDATION')                     
                  ]
    home_ownership = models.CharField(max_length=10,choices=OWNERSHIP_CHOICES)
    emp_length = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(43)])
    loan_amount = models.FloatField(validators=[MinValueValidator(0.0),
                                       MaxValueValidator(40000.0)])
    person_age = models.PositiveIntegerField(validators=[MinValueValidator(18),
                                       MaxValueValidator(110)])
    income = models.FloatField(validators=[MinValueValidator(1000.0),
                                       MaxValueValidator(7000000.0)])
    loan_intent = models.CharField(max_length=20,choices=INTENTIONS)
    applicant_details = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    managed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    
class LoanDetails(models.Model):
    LOAN_GRADES = [
        ("A","A"),
        ("B","B"),
        ("C","C"),
        ("D","D"),
        ("E","E"),
        ("F","F"),
        ("G","G")
    ]
    # credit history ranges from 2 to 30
    credit_history = models.PositiveIntegerField(validators=[MinValueValidator(2),
                                       MaxValueValidator(35)])
    credit_default = models.BooleanField()
    interest_rate = models.FloatField(validators=[MinValueValidator(4.0),
                                       MaxValueValidator(24.0)])
    grade = models.CharField(max_length=3, choices=LOAN_GRADES)
    loan_percent_to_income = models.FloatField(validators=[MinValueValidator(0.0),
                                       MaxValueValidator(0.84)])
    loan_request = models.OneToOneField(Loan, on_delete= models.CASCADE)
    

class LoanPrediction(models.Model):
    prediction_status = models.BooleanField(default=False)
    loan_status = models.BooleanField(null=True,default=None)
    loan_data = models.OneToOneField(Loan, on_delete =  models.CASCADE)
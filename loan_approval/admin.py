from django.contrib import admin
from .models import Applicant, Employee, Loan, LoanDetails, LoanPrediction

# Register your models here.
admin.site.register(Applicant)  
admin.site.register(Employee)
admin.site.register(Loan)
admin.site.register(LoanDetails)
admin.site.register(LoanPrediction)
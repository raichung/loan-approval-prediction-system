from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Loan, LoanDetails, LoanPrediction

class ApplicantModelForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['email','username','password1','password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        return email    
    
    def save(self, commit=True):
        user = super(ApplicantModelForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # print(user.email)
        if commit:
            user.save()
        return user
    
    
class EmployeeModelForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['email','username','password1','password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        return email    
    
    def save(self, commit=True):
        user = super(EmployeeModelForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # print(user.email)
        user.is_staff = True
        if commit:
            user.save()
        return user
    
    
class LoanRequestModelForm(forms.ModelForm):
    class Meta:
        model = Loan
        # fields = "__all__"
        exclude = ['applicant_details',]
        
        def clean_emp_length(self):
            data = self.cleaned_data.get("emp_length")
            if data<0 and data>43:
                print("Invalid")
                raise ValidationError("Employment length must be within 0 to 43 years.")
            else:
                return data
        def clean_person_age(self):
            data = self.cleaned_data.get("person_age")
            if data<18 and data>110:
                print("Invalid")
                raise ValidationError("Age must be within 0 to 110 years.")
            else:
                return data        
        
        def clean_loan_amount(self):
            data = self.cleaned_data.get('loan_amount')
            if data<0.0 and data>40000.0:
                raise ValidationError("Loan amount must be within 0.0 to 40000.0")
            else:
                return data
            
        def clean_income(self):
            data = self.cleaned_data["income"]
            if data<1000.0 and data>7000000.0:
                raise ValidationError("Income must be within 1000.0 to 7000000.0")
            else:
                return data
           
        
class LoanDetailsModelForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        # fields = ['exclude']
        exclude = ['loan_request']
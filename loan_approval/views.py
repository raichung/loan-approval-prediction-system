from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse  
from .models import Loan, Applicant, Employee, LoanDetails, LoanPrediction
from .forms import LoanRequestModelForm,ApplicantModelForm, EmployeeModelForm, LoanDetailsModelForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Class Based views 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from .utils import Model
from .populate_database import Loader

# Create your views here.
# def hello_world(request):
#     return HttpResponse("Hello World "+str(request.user));

def index(request):
    l = Loader()
    l.load_csv()
    # l.split_columns()
    return render(request, 'loan_approval/index.html',{})

def dashboard(request):
    return render(request, 'loan_approval/dashboard.html',{})

def about(request):
    return render(request, 'loan_approval/about.html',{})

def contact(request):
    return render(request, 'loan_approval/contact.html',{})

def working(request):
    return render(request, 'loan_approval/howitworks.html',{})

def visualization(request):
    return render(request,'loan_approval/visualization.html',{})

# def apply_now(request):
#     return render(request, 'loan_approval/about.html',{})
# User Registration
def applicant_register(request): 
    if request.method == "POST":
        user_form = ApplicantModelForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            applicant = user_form.save()
            Applicant.objects.create(applicant= applicant)
            print("applicant created sucessfully.")
            return redirect('loan_approval:user_login')
    elif request.method =="GET":
        user_form = ApplicantModelForm()
    context = {'form':user_form}
    return render(request, 'loan_approval/applicant_registration.html',context)

def employee_register(request): 
    if request.method == "POST":
        user_form = EmployeeModelForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            employee = user_form.save()
            Employee.objects.create(employee=employee)
            print("applicant created sucessfully.")
            return redirect('loan_approval:user_login')
    elif request.method =="GET":
        user_form = EmployeeModelForm()
    context = {'form':user_form}
    # TODO : change the applicant_registration form after front end submission. 
    return render(request, 'loan_approval/employee_registration.html',context)
    

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'loan_approval/login.html'
    def get_success_url(self):
        return reverse_lazy('loan_approval:dashboard') 
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('loan_approval:index')

@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanRequestCreateView(CreateView):
    model = Loan
    form_class = LoanRequestModelForm
    success_url = reverse_lazy('loan_approval:applicant_loan_list')
    template_name = 'loan_approval/applicant_loan_request_form.html'
    
    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.applicant_details = self.request.user.applicant
        return super().form_valid(form)
        
        
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanRequestListView(ListView):
    model = Loan
    template_name = 'loan_approval/applicant_loan_request.html'
    
    def get_queryset(self):
        queryset = self.model._default_manager.all()
        try:
            user = self.request.user.applicant
        except:
            return queryset
        else:
            return queryset.filter(applicant_details = user)
    
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanListView(ListView):
    model = Loan
    template_name = 'loan_approval/employee_loan_request.html'
    
    def get_queryset(self):
        queryset = self.model._default_manager.all()
        try:
            user = self.request.user.employee
        except:
            return queryset
        else:
            return queryset.filter(managed_by = user)

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def loanDetailsCreateView(request,pk):
    context = {}
    queryset = Loan.objects.get(id=pk)
    if request.method == "GET":
        context['home_ownership'] = queryset.home_ownership
        context['emp_length'] = queryset.emp_length
        context['loan_amount'] = queryset.loan_amount
        context['person_age'] = queryset.person_age
        context['income'] = queryset.income
        context['loan_intent'] = queryset.loan_intent
        context['id'] = pk
        context['interest_rate'] = 12
        context['loan_percent_to_income']= queryset.loan_amount/queryset.income
        context['grade'] = "A"
        # print(queryset.managed_by, queryset.applicant_details)
        #form = LoanDetailsModelForm()
        # context['form'] = form
        return render(request, 'loan_approval/loan_details_form.html',context)
    elif request.method == "POST":
        print("POST")
        id = pk
        # print(id)
        # form = LoanDetailsModelForm(request.POST)
        context['home_ownership'] = queryset.home_ownership
        context['emp_length'] = queryset.emp_length
        context['loan_amount'] = queryset.loan_amount
        context['person_age'] = queryset.person_age
        context['income'] = queryset.income
        context['loan_intent'] = queryset.loan_intent
        context['id'] = pk
        #context['form'] = form

        credit_history = request.POST.get('credit_history')
        credit_default = request.POST.get('credit_default')
        interest_rate = request.POST.get('interest_rate')
        grade = request.POST.get('grade')
        loan_percent_to_income = request.POST.get('loan_percent_to_income')     

        print(f"credit history is {credit_history}")
        print(f"credit default is {credit_default}")
        print(f"interest is : {interest_rate}")
        print(f"grade  is : {grade}")
        print(f" loan_percent to income is : {loan_percent_to_income}")

        
        loan_details = LoanDetails()
        # print(form.cleaned_data)
        loan_details.loan_request = queryset
        # print(queryset.loan_amount/queryset.income)
        loan_details.interest_rate = 12
        loan_details.grade = "A"
        loan_details.interest_rate = float(interest_rate)
        loan_details.credit_default = True
        loan_details.credit_history = int(credit_history)
        loan_details.loan_percent_to_income = queryset.loan_amount/queryset.income
        loan_details.save()

        print(queryset)
        model = create_model(queryset)
        loan_status = model.predict_data()
        prediction = LoanPrediction.objects.create(loan_data=queryset, loan_status=loan_status, prediction_status=True)
        print(f"prediction is {prediction}")
        prediction.save()
        return redirect('loan_approval:index')
    
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanDetailsListView(ListView):
    model = LoanDetails
    template_name = 'loan_approval/loan_details_list.html'
    
    def get_queryset(self):
        queryset = self.model._default_manager
        try:
            user = self.request.user.employee
        except:
            print("User is applicant.")
        else:
            # loan = LoanDetails.objects.filter(loan_request__managed_by = employee)
            return queryset.filter(loan_request__managed_by = user)
        try:
            user = self.request.user.applicant
            # print("Applicant view")
        except:
            print("User is employee.")
        else:
            # loan = LoanDetails.objects.filter(loan_request__managed_by = employee)
            return queryset.filter(loan_request__applicant_details = user)

@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanDetailsDetailView(DetailView):
    model = LoanDetails
    template_name = 'loan_approval/detailed_loan_details_.html'

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def update_loan_request(request,id):
    if request.method =="GET":
        obj = get_object_or_404(Loan, id=id)
        form = LoanRequestModelForm(request.GET or None, instance = obj)
        return render(request, 'loan_approval/loan_update.html',{"form":form})
    elif request.method =="POST":
        # loan = Loan.objects.get(id = id)
        loan_details = LoanDetails.objects.filter(loan_request__id = id)
        if loan_details:
            print(loan_details)
            loan_details.delete()
            print("Object deleted.")
        obj = get_object_or_404(Loan, id=id)
        form = LoanRequestModelForm(request.POST or None, instance = obj)
        if form.is_valid():
            print(form)
            form.save()
        else:
            return render(request, 'loan_approval/loan_update.html',{"form":form})
        return redirect("loan_approval:applicant_loan_list")

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def delete_loan(request,id):
    # fetch the object related to passed id
    if request.user.is_authenticated:
        condition1 = request.user.is_staff
        condition2 = request.user.is_superuser
        print(condition1, condition2)
        if not (condition1 or condition2):
            obj = get_object_or_404(Loan, id = id)
            # delete object
            obj.delete()
            # after deleting redirect to home page.
            return redirect("loan_approval:applicant_loan_list")
        else:
            return HttpResponse("<h3> SuperAdmin or Employee cannot delete loan request. </h3>")

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def update_loan_details(request,pk):
    context = {}
    obj = get_object_or_404(LoanDetails, id = pk)
    context['home_ownership'] = obj.loan_request.home_ownership
    context['emp_length'] = obj.loan_request.emp_length
    context['loan_amount'] = obj.loan_request.loan_amount
    context['person_age'] = obj.loan_request.person_age
    context['income'] = obj.loan_request.income
    context['loan_intent'] = obj.loan_request.loan_intent
    if request.method == "GET":        
        form = LoanDetailsModelForm(request.GET or None, instance = obj)
        # form = LoanDetailsModelForm()
        context['form'] = form
        return render(request, 'loan_approval/loan_details_form.html',context)
    elif request.method == "POST":
        form = LoanDetailsModelForm(request.POST or None, instance = obj)
        context['form'] = form
        if form.is_valid():
            print("Form is valid.")
            # print(form)
            form.save()
            return redirect("loan_approval:applicant_loan_list")
        else:
            return render(request, 'loan_approval/loan_details_form.html',context)

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def predict(request,pk):
    # print(not request.user.is_superuser)
    condition1 = request.user.is_superuser
    condition2 = request.user.is_authenticated
    # print(condition1 and condition2 ) 
    if  condition2:
    # Function used by machine learning.
        if condition1:
            context = {}
            context['error'] = "403: Super user cannot look after loan approval prediction."
            return JsonResponse(context, status=403)
        else:
            """
            obj = get_object_or_404(Loan, id = pk)
            print(obj)
            model = create_model(obj)
            loan_status = model.predict_data()

            print(f"loan status is {loan_status}")
            # Pipelining and others.
            # print(obj.loanprediction)
            prediction_status = True
            #prediction_object = obj.loanprediction
            prediction_object  = LoanPrediction.objects.get_or_create(loan_data = Loan)
            print("are we here")
            # print(prediction_object)
            prediction_object.prediction_status = prediction_status
            prediction_object.loan_status = loan_status
            prediction_object.save()
            loan_instance, created = Loan.objects.get_or_create(**obj)

            # Check if a LoanPrediction object with the obtained Loan instance exists
            loan_prediction = LoanPrediction.objects.filter(loan_data=obj).first()

            # If a LoanPrediction object doesn't exist, create a new one
            if not loan_prediction:
                loan_prediction = LoanPrediction.objects.create(
                    prediction_status=True,  # Set prediction status as needed
                    loan_status=loan_status,  # Set loan status based on loan data
                    loan_data=obj  # Set the loan_data foreign key field to the Loan instance
                )
            else:
                loan_status = loan_prediction.loan_status
            """

            obj = get_object_or_404(Loan, id=pk)

            # Check if a LoanPrediction object with the obtained Loan instance exists
            loan_prediction = LoanPrediction.objects.filter(loan_data=obj).first()

            loan_status = True
            if loan_prediction:
                # LoanPrediction object already exists, retrieve loan_status
                loan_status = loan_prediction.loan_status
            else:
                # LoanPrediction object doesn't exist, perform prediction and create new object
                model = create_model(obj)
                loan_status = model.predict_data()

                # Create a new LoanPrediction instance with loan_data set to the obtained Loan instance
                loan_prediction = LoanPrediction.objects.create(
                    prediction_status=True,  # Set prediction status as needed
                    loan_status=loan_status,  # Set loan status based on prediction
                    loan_data=obj  # Set the loan_data foreign key field to the Loan instance
                )

            # Optionally, you can redirect to another page or return a response

            # prediction_object.objects.update(prediction_status = True, loan_status= loan_status)    
            context = {}
            context['prediction']  = loan_status
            # print(context)
            return JsonResponse(context, status=200)
    else:
        context = {}
        context['error'] = "404:  cannot view loan approval prediction."
        return JsonResponse(context, status=404)
        

def create_model(loan):
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
    print(person_age,income,intent,emp_length,amount,ownership,credit_history,rate,default,grade,percent_to_income)
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

def return_loan_credit_history(request):
    employee = request.user.employee
    credit_history = {}
    loans = Loan.objects.filter(managed_by=employee)
    for i  in range(len(loans)):
        try:
            loandetails = loans[i].loandetails
        except:
            print("Exception found.")
            pass
        else:
            hist = loandetails.credit_history 
            # print()
            if hist in credit_history.keys():
                credit_history[hist]+=1
            else:
                credit_history[hist] = 1
    print(credit_history)
    context = {}
    context['credit_history'] = credit_history
    return JsonResponse(context, status=200)

def return_loan_predictions(request):
    if request.user.is_superuser== False and request.user.is_staff == True:
        employee = request.user.employee
        loan_prediction = {}
        loans = Loan.objects.filter(managed_by=employee)
        for i  in range(len(loans)):
            try:
                loanprediction = loans[i].loanprediction
            except:
                pass
            else:
                prediction = loanprediction.loan_status 
                # print()
                if prediction in loan_prediction.keys():
                    loan_prediction[prediction]+=1
                else:
                    loan_prediction[prediction] = 1
        # print(credit_history)
        context = {}
        context['loan_prediction'] = loan_prediction
        return JsonResponse(context, status=200)
    else:
        context['error'] = {"403":"User not authorized."}
        return JsonResponse(context, status = 403)

def return_home_ownership(request):
    context = {}
    if request.user.is_superuser== False and request.user.is_staff == True:
        employee = request.user.employee
        homeownership = {}
        loans = Loan.objects.filter(managed_by=employee)
        for i in range(len(loans)):
            ownership = loans[i].home_ownership
            if ownership in homeownership.keys():
                homeownership[ownership]+=1
            else:
                homeownership[ownership]=1
        context['home_ownership'] = homeownership
        return JsonResponse(context, status = 200)
    else:
        context['error'] = {"403":"User not authorized."}
        return JsonResponse(context, status=403)

def return_intent(request):
    context = {}
    if request.user.is_superuser== False and request.user.is_staff == True:
        employee = request.user.employee
        loan_intent = {}
        loans = Loan.objects.filter(managed_by=employee)
        for i in range(len(loans)):
            intent = loans[i].loan_intent
            if intent in loan_intent.keys():
                loan_intent[intent]+=1
            else:
                loan_intent[intent]=1
        context['loan_intent'] = loan_intent
        return JsonResponse(context, status = 200)
    else :
        context['error'] = {"403":"User not authorized."}
        return JsonResponse(context, status=403)

def dummy(request):
    return render(request,"loan_approval/dummy.html", {})

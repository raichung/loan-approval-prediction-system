from django.urls import path
from .views import (index,dashboard,about,working, contact, applicant_register, 
                    employee_register, logout, loanDetailsCreateView, update_loan_request, 
                    delete_loan, update_loan_details, predict, return_loan_credit_history,
                    return_home_ownership,return_intent,dummy, 
                    return_loan_predictions,visualization)
from .views import LoanRequestCreateView, UserLoginView, LoanRequestListView, LoanListView, LoanDetailsListView, LoanDetailsDetailView
from django.contrib.auth.views import LogoutView

app_name = "loan_approval"
urlpatterns = [
    path('',index,name="index"),
    path('dashboard/',dashboard, name="dashboard"),
    path("about/",about, name="about"),
    path("how-it-works/",working, name="working"),
    path("contact/",contact, name="contact"),
    path('applicant/register/',applicant_register,name='applicant_register'),
    path('employee/register/',employee_register,name='employee_register'),
    # Users related activities.
    path('user/login/',UserLoginView.as_view(),name='user_login'),
    path('user/logout/', LogoutView.as_view(next_page='loan_approval:index'), name='user_logout'),
    # Loan request related routes
    path('loan/request/',LoanRequestCreateView.as_view(),name="loan_request"),
    path('loan/list/',LoanRequestListView.as_view(), name='applicant_loan_list'),
    path('loan/update/<int:id>/',update_loan_request, name='loan_update'),
    path("loan/delete/<int:id>/",delete_loan, name='loan_delete'),
    
    # Employee related scenarios
    path('loan/',LoanListView.as_view(), name='employee_loan_list'),
    path("loan-details/create/<int:pk>/",loanDetailsCreateView, name='loan_details_create'),
    path("loan-details/<int:pk>/",LoanDetailsDetailView.as_view(), name="loan_details_detail"),
    path('loan-details/update/<int:pk>/',update_loan_details,name='loan_details_update'),
    # Both Perspective
    path("loan-details/",LoanDetailsListView.as_view(),name="loans_details_list"),
    path("loan/predict/<int:pk>/",predict, name='predict'),
    # Visualization related works
    path('visualization/', visualization, name='visualize'),
    path("visualization/credit-history/",return_loan_credit_history, name="visualize-cr-hist"),
    path("visualization/loan-prediction/",return_loan_predictions, name="visualize-loan-pred"),
    path("visualization/home-ownership/",return_home_ownership, name="visualize-home-ownership"),
    path("visualization/loan-intent/",return_intent,name="visualize-loan-intent"),
    path("dummy/",dummy,name='dummy'),
]

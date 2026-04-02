from django.urls import path
from . import views

urlpatterns = [
    path('students/',views.studentsView,name="fetchallstudents"),
    path('students/<int:pk>/',views.studentDetailView,name="fetchonestudent"),      #accepting the primary key with this URL
    path('employees/',views.Employees.as_view())                # here we trying to treat the Employee class as a view
]
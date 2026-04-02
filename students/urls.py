from django.urls import path,include
from .views import *

urlpatterns = [
    path('',view=students,name="students")
]
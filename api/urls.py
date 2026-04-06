from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees',views.EmployeeViewset,basename="employee")

urlpatterns = [
    path('students/',views.studentsView,name="fetchallstudents"),
    path('students/<int:pk>/',views.studentDetailView,name="fetchonestudent"),      #accepting the primary key with this URL
    # path('employees/',views.Employees.as_view()),                # here we trying to treat the Employee class as a view
    # path('employees/<str:pk>',views.EmployeeDetails.as_view()),

    path('',include(router.urls)),
    path('blogs/',views.BlogsView.as_view()),
    path('comments/',views.CommentsView.as_view()),
    path('blogs/<int:pk>',views.BlogsDetailView.as_view()),
    path('comments/<int:pk>',views.CommentsDetailView.as_view()),
]
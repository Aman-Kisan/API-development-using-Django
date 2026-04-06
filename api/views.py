from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,response
from django.http import Http404

from django_filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets

from students.models import Student
from employees.models import Employee
from blogs.models import Comment,Blog
from blogs.serializers import BlogSerializer,CommentSerializer
from .serializers import StudentSerializer,EmployeeSerializer
from .paginations import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter,OrderingFilter


# function based views
@api_view(['GET'])              # this decorator allows the view to be used for GET method only
@permission_classes([AllowAny])  # This fixes the permission error as models are only allowed to be read by ViewSets
def studentsView(request):

    if request.method == 'GET':
        #get all the data from the student table
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset,many=True)      #many is set to True for telling that there are multiple instances of the model
        return Response(serializer.data,status=status.HTTP_200_OK)      # returning Response object of rest_framework module

    # Manual Serialization
    # students = Student.objects.all()
    # students_list = list(students.values())
    # return JsonResponse(students_list,safe=False)
    
    
    # for POST method
    serializer = StudentSerializer(data=request.data)       # here serielizer takes the data from the request object sent by client
    if serializer.is_valid():       # checking serializer is valid or not
        serializer.save()           # serializer saving data to DB
        return Response(serializer.data,status=status.HTTP_201_CREATED)     #sending the data that was entered in response
    else:
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# function based views
@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
def studentDetailView(request,pk):
    try:
        query_set= Student.objects.get(reg_no=pk)
        # student = get_object_or_404(Student, pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(query_set)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # for PUT method   not working properly avoid this 
    elif request.method == 'PUT':
        serializer = StudentSerializer(query_set,data=request.data,partial=True)      # this the way you populate the form so that it can be updated
        # print("Errors:", serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        query_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




# Manual ways to handle the GET,POST,PUT,DELETE request
# class based views
# @permission_classes([AllowAny]) 
# class Employees(APIView):

#     def get(self,request):
#         query_set = Employee.objects.all()
#         serializer = EmployeeSerializer(query_set,many = True)
#         return Response(serializer.data,status = status.HTTP_200_OK)
    
#     def post(self,request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class EmployeeDetails(APIView):

    # def get_object(self,pk):
    #     try:
    #         return Employee.objects.get(id=pk)
    #     except Employee.DoesNotExist:
    #         raise Http404                   # why this works not the return Response ?
        
    # def get(self,request,pk):
    #     query_set = self.get_object(pk)
    #     serializer = EmployeeSerializer(query_set)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
    # def put(self,request,pk):
    #     query_set = self.get_object(pk)
    #     serializer = EmployeeSerializer(query_set,data=request.data)            #intake the data from DB and data came with the request -- So that updation can be made for that data
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)
    
    # def delete(self,request,pk):
    #     query_set = self.get_object(pk)
    #     query_set.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

# Using the inbuild mixin and generic feature of Django the handle CRUD operation 

#this can be called as class-based Mixins views
'''
class Employees(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self,request):              #No need to write manual code for handling the get request i.e fetching the data
        return self.list(request)           
    
    def post(self,request):             #No need the check if it valid or not and no need to manually save and give response for success or bad request
        return self.create(request)     
'''    
#this can be called as class-based Mixins views
"""
class EmployeeDetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    
    queryset = Employee.objects.all()           #fetch all the instances of  the Employee model
    serializer_class = EmployeeSerializer       #set the serializer class

    def get(self,request,pk):                   
        return self.retrieve(request,pk)        # retrieve() automatically fetches the data based on the Primary Key
    
    def put(self,request,pk):
        return self.update(request,pk)         #update() comes from UpdateModelMixin
    
    def delete(self,request,pk):
        return self.destroy(request,pk)         #destroy() comes from DestroyModelMixin
"""





#class based generics views

# class Employees(generics.ListCreateAPIView):      #automatically returns a response
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
    

# class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = "pk"             #this attibute tells the class to search in the DB based on the given Primary Key value



#class based views using viewsets.ViewSet

# class EmployeeViewset(viewsets.ViewSet):

#     def list(self,request):
#         queryset = Employee.objects.all()
#         serializer = EmployeeSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors)
    
#     def retrieve(self,request,pk=None):
#         employee = get_object_or_404(Employee,pk=pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def update(self,request,pk=None):
#         employee = get_object_or_404(Employee,pk=pk)
#         serializer = EmployeeSerializer(employee,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     def delete(self,request,pk=None):
#         employee = get_object_or_404(Employee,pk=pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#class based views using viewsets.ModelViewSets

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination     #simply set the pagination class to CustomPagination class then ViewSet automatically handles it everything inside
    # filterset_fields = ['designation']
    filterset_class = EmployeeFilter


class BlogsView(generics.ListCreateAPIView): 
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['blog_title','blog_body']          #searching a blog based on a word that appeared in either blog_title or body
    # adding '^' before the field allows to search only those blogs that starts with that word
    ordering_fields = ['id']


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class BlogsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    

class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
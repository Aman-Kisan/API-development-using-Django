# from django.shortcuts import render
from django.http import JsonResponse,response
from students.models import Student
from employees.models import Employee
from .serializers import StudentSerializer,EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import Http404


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
    


# class based views
# @permission_classes([AllowAny]) 
class Employees(APIView):

    def get(self,request):
        query_set = Employee.objects.all()
        serializer = EmployeeSerializer(query_set,many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeDetails(APIView):

    def get_object(self,pk):
        try:
            return Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            raise Http404                   # why this works not the return Response ?
        
    def get(self,request,pk):
        query_set = self.get_object(pk)
        serializer = EmployeeSerializer(query_set)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        query_set = self.get_object(pk)
        serializer = EmployeeSerializer(query_set,data=request.data)            #intake the data from DB and data came with the request -- So that updation can be made for that data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        query_set = self.get_object(pk)
        query_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
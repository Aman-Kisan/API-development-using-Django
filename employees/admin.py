from django.contrib import admin
from .models import Employee

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):          # this way we decide how to view the Employee data on the admin site
    list_display = ['emp_id','emp_name','designation']
    list_filter = ['emp_id']

admin.site.register(Employee,EmployeeAdmin)
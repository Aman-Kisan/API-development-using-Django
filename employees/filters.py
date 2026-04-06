from xml.dom.minidom import CharacterData

import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(field_name='designation',lookup_expr='iexact')      #"iexact" matches the exact entered value
    emp_name = django_filters.CharFilter(field_name = 'emp_name',lookup_expr='icontains')     #"icontains" checks if the value is contained
    # emp_id = django_filters.RangeFilter(field_name='emp_id')        #only can be used if the field in INTEGER type

    id_min = django_filters.CharFilter(method='filter_by_id_range',label='From EMP ID')     #setting the label name is avoiding the [invalid name] tag
    id_max = django_filters.CharFilter(method='filter_by_id_range',label='To EMP ID')

    class Meta:
        model = Employee
        fields = ['designation','emp_name','id_min','id_max']       #id_min and id_max are not fields of the Model

    def filter_by_id_range(self,queryset,name,value):       # this is a method used for manual Range filter
        if name == 'id_min':
            return queryset.filter(emp_id__gte=value)
        elif name == 'id_max':
            return queryset.filter(emp_id__lte=value)
        return queryset
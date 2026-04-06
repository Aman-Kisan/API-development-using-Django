"""This file is for Custom Pagination
Instead of sending all the JSON data to client at once
we can send it in chunks i.e as much required (it can be 5 or 10 datas at a time)
The Global Pagination works on all the APIs
But we can control some by using Custom Pagination

Here the Global Pagination is working on LimitOffset conditions

We are creating here a Custom Pagination that works on page system

Page Size = 2 remains same as the Global in settings

"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    #over-riding attributes for manual changes
    page_size_query_param = 'page_size'
    page_query_param = "page-num"
    max_page_size = 1

    #over-riding function for manual changes
    def get_paginated_response(self, data):
        return Response({
                "next": self.get_next_link(),
                "previous":self.get_previous_link(),
                "count": self.page.paginator.count,
                "page_size":self.page_size,
                "results":data
            })

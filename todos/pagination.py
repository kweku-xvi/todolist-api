from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'count'
    max_page_size = 5
    page_query_param = 'p'
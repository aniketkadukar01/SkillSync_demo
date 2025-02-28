from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    """
    This Pagination is used on User details it will limit the data which is displayed.
    """
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 15

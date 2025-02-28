from rest_framework.pagination import PageNumberPagination

class AssigneePagination(PageNumberPagination):
    """
    This Pagination is used on Assignee details it will limit the data which is displayed.
    """
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 15

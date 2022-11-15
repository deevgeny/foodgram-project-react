from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Customized PageNumberPatinaion.

    Allow user pass 'limit' parameter in request to set page size limit.
    For example: data={'limit': 5} will return pages with 5 items.
    """
    
    page_size_query_param = 'limit'

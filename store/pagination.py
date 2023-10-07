from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class ProductPagination(PageNumberPagination):
    page_size = 10


class CustomerPagination(PageNumberPagination):
    page_size = 10
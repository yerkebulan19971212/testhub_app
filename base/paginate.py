from rest_framework.pagination import PageNumberPagination


class FlashCardsPaginate(PageNumberPagination):
    page_size = 1
    max_page_size = 100

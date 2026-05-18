from rest_framework.pagination import LimitOffsetPagination


class HabitPagination(LimitOffsetPagination):
    """
    Пагинация для привычек - 5 штук на страницу с limit/offset
    Пример: /api/habits/?limit=5&offset=0
    """
    default_limit = 5
    max_limit = 50
    limit_query_param = 'limit'
    offset_query_param = 'offset'

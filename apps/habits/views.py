from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from .models import Habit, HabitExecution
from .serializers import HabitSerializer, HabitPublicSerializer, HabitExecutionSerializer
from .permissions import IsOwner
from .pagination import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_pleasant', 'periodicity', 'is_public']
    search_fields = ['action', 'place']
    ordering_fields = ['time', 'created_at']
    ordering = ['time']

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Получить список публичных привычек",
        responses={200: HabitPublicSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='public')
    def public_habits(self, request):
        """Список публичных привычек"""
        public_habits = Habit.objects.filter(is_public=True).exclude(user=request.user)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = HabitPublicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = HabitPublicSerializer(public_habits, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Переключить статус публичности привычки",
        responses={200: openapi.Response('Статус обновлен')}
    )
    @action(detail=True, methods=['post'], url_path='toggle-public')
    def toggle_public(self, request, pk=None):
        """Переключение статуса публичности"""
        habit = self.get_object()
        habit.is_public = not habit.is_public
        habit.save()
        return Response({'is_public': habit.is_public})

    @swagger_auto_schema(
        operation_description="Получить историю выполнения привычки",
        responses={200: HabitExecutionSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='executions')
    def executions(self, request, pk=None):
        """История выполнения привычки"""
        habit = self.get_object()
        executions = HabitExecution.objects.filter(habit=habit).order_by('-execution_date')
        page = self.paginate_queryset(executions)
        if page is not None:
            serializer = HabitExecutionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = HabitExecutionSerializer(executions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Отметить выполнение привычки",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'execution_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                'notes': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={201: HabitExecutionSerializer()}
    )
    @action(detail=True, methods=['post'], url_path='complete')
    def complete_habit(self, request, pk=None):
        """Отметить выполнение привычки"""
        habit = self.get_object()
        execution_date = request.data.get('execution_date', date.today())
        notes = request.data.get('notes', '')

        execution, created = HabitExecution.objects.get_or_create(
            habit=habit,
            execution_date=execution_date,
            defaults={'status': 'completed', 'notes': notes}
        )

        if not created and execution.status != 'completed':
            execution.status = 'completed'
            execution.completed_at = None
            execution.notes = notes
            execution.save()

        serializer = HabitExecutionSerializer(execution)
        return Response(serializer.data, status=status.HTTP_200_OK)

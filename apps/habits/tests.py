from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import time, date
from .models import Habit, HabitExecution

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_create_habit_success(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(9, 0),
            action='Morning run',
            execution_time=60,
            periodicity='daily'
        )
        self.assertEqual(habit.action, 'Morning run')
        self.assertEqual(habit.place, 'Home')
        self.assertFalse(habit.is_pleasant)

    def test_habit_execution_time_validation(self):
        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.user,
                place='Home',
                time=time(9, 0),
                action='Too long',
                execution_time=121,
                periodicity='daily'
            )

    def test_habit_reward_and_related_cannot_together(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Anywhere',
            time=time(10, 0),
            action='Meditate',
            execution_time=60,
            is_pleasant=True,
            periodicity='daily'
        )

        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.user,
                place='Office',
                time=time(14, 0),
                action='Work',
                execution_time=30,
                reward='Chocolate',
                related_habit=pleasant_habit,
                periodicity='daily'
            )

    def test_pleasant_habit_no_reward(self):
        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.user,
                place='Home',
                time=time(20, 0),
                action='Watch movie',
                execution_time=60,
                reward='Popcorn',
                is_pleasant=True,
                periodicity='daily'
            )


class HabitAPITestCase(APITestCase):
    """Тесты API привычек"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(9, 0),
            action='Morning run',
            execution_time=60,
            periodicity='daily'
        )

    def test_list_habits(self):
        url = '/api/habits/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_habit_success(self):
        url = '/api/habits/habits/'
        data = {
            'place': 'Office',
            'time': '14:00:00',
            'action': 'Drink water',
            'execution_time': 30,
            'periodicity': 'daily'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_habit_invalid_execution_time(self):
        url = '/api/habits/habits/'
        data = {
            'place': 'Gym',
            'time': '18:00:00',
            'action': 'Workout',
            'execution_time': 180,
            'periodicity': 'daily'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_habit(self):
        url = f'/api/habits/habits/{self.habit.id}/'
        data = {'action': 'Evening run'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Evening run')

    def test_delete_habit(self):
        url = f'/api/habits/habits/{self.habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_public_habits(self):
        url = '/api/habits/habits/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_toggle_public(self):
        url = f'/api/habits/habits/{self.habit.id}/toggle-public/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertTrue(self.habit.is_public)

    def test_complete_habit(self):
        url = f'/api/habits/habits/{self.habit.id}/complete/'
        response = self.client.post(url, {'execution_date': date.today()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        execution = HabitExecution.objects.filter(habit=self.habit).first()
        self.assertIsNotNone(execution)
        self.assertEqual(execution.status, 'completed')

    def test_other_user_cannot_access_habit(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        self.client.force_authenticate(user=other_user)

        url = f'/api/habits/habits/{self.habit.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserAPITestCase(APITestCase):
    """Тесты API пользователей"""

    def test_register_user(self):
        url = '/api/users/register/'
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        User.objects.create_user(
            email='login@example.com',
            username='loginuser',
            password='testpass123'
        )

        url = '/api/users/login/'
        data = {
            'email': 'login@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        url = '/api/habits/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PaginationTestCase(APITestCase):
    """Тесты пагинации"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Создаем 12 привычек (больше чем default_limit=5)
        for i in range(12):
            Habit.objects.create(
                user=self.user,
                place=f'Place {i}',
                time=time(12, i % 60),
                action=f'Action {i}',
                execution_time=60,
                periodicity='daily'
            )

    def test_pagination_limit_offset(self):
        """Тест пагинации с limit и offset"""
        url = '/api/habits/habits/?limit=5&offset=0'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 12)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_pagination_second_page(self):
        """Тест второй страницы пагинации"""
        url = '/api/habits/habits/?limit=5&offset=5'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 12)

        # Проверяем, что вторая страница содержит другие элементы
        first_page = self.client.get('/api/habits/habits/?limit=5&offset=0').data['results']
        second_page = response.data['results']
        first_ids = [item['id'] for item in first_page]
        second_ids = [item['id'] for item in second_page]
        self.assertNotEqual(first_ids, second_ids)

    def test_pagination_default_limit(self):
        """Тест пагинации с лимитом по умолчанию (5)"""
        url = '/api/habits/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 12)

    def test_pagination_custom_limit(self):
        """Тест пагинации с кастомным лимитом"""
        url = '/api/habits/habits/?limit=3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['count'], 12)

    def test_pagination_last_page(self):
        """Тест последней страницы пагинации"""
        url = '/api/habits/habits/?limit=5&offset=10'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 12)

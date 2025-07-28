from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Subscription, Course

User = get_user_model()


class SubscriptionAPITests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create(
            email='user1@example.com',
            password='testpass'
        )
        self.user2 = User.objects.create(
            email='user2@example.com',
            password='testpass'
        )

        # Создаем курсы
        self.course1 = Course.objects.create(name='Course 1', description='Test')
        self.course2 = Course.objects.create(name='Course 2', description='Test')

        # URL для операций
        self.create_url = '/users/subscriptions/'
        self.delete_url = '/users/subscriptions/{course_id}/'

    # Тесты для создания подписок (SubscriptionCreateView)
    def test_create_subscription_success(self):
        """Успешное создание подписки"""
        self.client.force_authenticate(user=self.user1)
        data = {'course': self.course1.id}

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем ответ
        self.assertEqual(response.data['user'], self.user1.id)
        self.assertEqual(response.data['course'], self.course1.id)
        self.assertTrue(response.data['is_active'])

        # Проверяем создание в БД
        subscription = Subscription.objects.get()
        self.assertEqual(subscription.user, self.user1)
        self.assertEqual(subscription.course, self.course1)
        self.assertTrue(subscription.is_active)

    def test_create_duplicate_subscription_fails(self):
        """Нельзя создать дубликат подписки"""
        # Создаем существующую подписку
        Subscription.objects.create(
            user=self.user1,
            course=self.course1,
            is_active=True
        )

        self.client.force_authenticate(user=self.user1)
        data = {'course': self.course1.id}

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            "Подписка на этот курс уже существует"
        )
        self.assertEqual(Subscription.objects.count(), 1)  # Новой подписки не создано

    def test_create_subscription_unauthenticated(self):
        """Неавторизованный пользователь не может создать подписку"""
        data = {'course': self.course1.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Тесты для удаления подписок (SubscriptionDeleteView)
    def test_delete_subscription_success(self):
        """Успешное удаление (деактивация) подписки"""
        # Создаем подписку для удаления
        subscription = Subscription.objects.create(
            user=self.user1,
            course=self.course1,
            is_active=True
        )

        self.client.force_authenticate(user=self.user1)
        url = self.delete_url.format(course_id=self.course1.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что подписка деактивирована
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)

    def test_delete_non_existent_subscription(self):
        """Попытка удалить несуществующую подписку"""
        self.client.force_authenticate(user=self.user1)
        url = self.delete_url.format(course_id=999)  # Несуществующий курс

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Подписка на этот курс не найдена")

    def test_delete_another_users_subscription(self):
        """Попытка удалить чужую подписку"""
        # Создаем подписку для user2
        Subscription.objects.create(
            user=self.user2,
            course=self.course1,
            is_active=True
        )

        self.client.force_authenticate(user=self.user1)
        url = self.delete_url.format(course_id=self.course1.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверяем, что подписка осталась активной
        subscription = Subscription.objects.get()
        self.assertTrue(subscription.is_active)

    def test_delete_subscription_unauthenticated(self):
        """Неавторизованный пользователь не может удалить подписку"""
        url = self.delete_url.format(course_id=self.course1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_already_inactive_subscription(self):
        """Попытка удалить уже неактивную подписку"""
        # Создаем неактивную подписку
        Subscription.objects.create(
            user=self.user1,
            course=self.course1,
            is_active=False
        )

        self.client.force_authenticate(user=self.user1)
        url = self.delete_url.format(course_id=self.course1.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
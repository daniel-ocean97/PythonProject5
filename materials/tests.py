from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson


class LessonAPITests(APITestCase):
    def setUp(self):
        # Создаем группы и пользователей
        self.manager_group = Group.objects.create(name="Managers")

        self.user1 = User.objects.create(email="user1@example.com", password="testpass")
        self.user2 = User.objects.create(email="user2@example.com", password="testpass")
        self.manager = User.objects.create(
            email="manager@example.com", password="testpass"
        )
        self.manager.groups.add(self.manager_group)

        self.course1 = Course.objects.create(name="Course 1", description="test")
        self.course2 = Course.objects.create(name="Course 2", description="test")
        self.course3 = Course.objects.create(name="Course 3", description="test")

        # Создаем тестовые уроки
        self.lesson1 = Lesson.objects.create(
            name="Lesson 1",
            description="Content 1",
            owner=self.user1,
            course=self.course1,  # Добавляем привязку к курсу
        )
        self.lesson2 = Lesson.objects.create(
            name="Lesson 2",
            description="Content 2",
            owner=self.user2,
            course=self.course2,  # Добавляем привязку к курсу
        )
        self.lesson3 = Lesson.objects.create(
            name="Lesson 3",
            description="Content 3",
            owner=self.user1,
            course=self.course3,  # Добавляем привязку к курсу
        )

        # URL для операций
        self.list_url = "/api/lessons/"
        self.detail_url = f"/api/lessons/{self.lesson1.id}/"

    # Тесты для LessonListCreateAPIView
    def test_manager_sees_all_lessons(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_user_sees_only_own_lessons(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        names = {lesson["name"] for lesson in response.data["results"]}
        self.assertIn("Lesson 1", names)
        self.assertIn("Lesson 3", names)

    def test_manager_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.manager)
        data = {
            "name": "New Lesson",
            "description": "New Content",
            "course": self.course1.id,  # Добавляем ID курса
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Managers cannot create lessons")

    def test_user_can_create_lesson(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "User Lesson",
            "description": "User Content",
            "course": self.course1.id,  # Добавляем ID курса
            "video": "https://www.youtube.com/watch?v=lknxOJseu0c&list=PLXtiZNKIobF4whGIJ8oVNtidZRDpRirDl",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 4)
        self.assertEqual(Lesson.objects.last().owner, self.user1)
        self.assertEqual(Lesson.objects.last().course.id, self.course1.id)

    # Тесты для LessonRetrieveUpdateDestroyAPIView
    def test_manager_can_view_any_lesson(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Lesson 1")

    def test_owner_can_view_own_lesson(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_view_lesson(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_can_update_any_lesson(self):
        self.client.force_authenticate(user=self.manager)
        data = {"name": "Updated name"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.name, "Updated name")

    def test_owner_can_update_own_lesson(self):
        self.client.force_authenticate(user=self.user1)
        data = {"description": "Updated Content"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.description, "Updated Content")

    def test_manager_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Managers cannot delete lessons")

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_non_owner_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



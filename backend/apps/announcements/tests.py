from rest_framework import status
from rest_framework.test import APITestCase

from apps.announcements.models import Announcement
from apps.users.models import User


class AnnouncementAdminManagementTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_announcement',
            password='pass1234',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        self.teacher = User.objects.create_user(username='teacher_announcement', password='pass1234', role='teacher')
        self.student = User.objects.create_user(username='student_announcement', password='pass1234', role='student')
        self.list_url = '/api/announcements/'

        self.payload = {
            'title': '系统维护通知',
            'content': '<p>本周末维护升级</p>',
            'is_published': True,
        }

    def test_admin_can_create_announcement(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.list_url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertEqual(Announcement.objects.first().author_id, self.admin.id)

    def test_teacher_cannot_create_announcement(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(self.list_url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Announcement.objects.count(), 0)

    def test_student_cannot_create_announcement(self):
        self.client.force_authenticate(self.student)
        response = self.client.post(self.list_url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Announcement.objects.count(), 0)

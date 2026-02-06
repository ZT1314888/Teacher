from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class UserAdminManagementTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_user_mgmt',
            password='pass1234',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        self.teacher = User.objects.create_user(
            username='teacher_user_mgmt',
            password='pass1234',
            role='teacher',
            email='teacher@example.com',
        )
        self.student = User.objects.create_user(
            username='student_user_mgmt',
            password='pass1234',
            role='student',
            email='student@example.com',
        )

    def test_admin_can_update_other_user_profile(self):
        self.client.force_authenticate(self.admin)
        response = self.client.patch(
            f'/api/users/{self.teacher.id}/',
            {'phone': '13800138000'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.phone, '13800138000')

    def test_teacher_cannot_update_other_user_profile(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.patch(
            f'/api/users/{self.student.id}/',
            {'phone': '13900139000'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.student.refresh_from_db()
        self.assertNotEqual(self.student.phone, '13900139000')

    def test_frontend_registration_cannot_create_admin_role(self):
        response = self.client.post(
            '/api/users/',
            {
                'username': 'hacker_admin',
                'email': 'hack@example.com',
                'password': 'pass1234',
                'password_confirm': 'pass1234',
                'role': 'admin',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('不能通过前端注册管理员账号', str(response.data))

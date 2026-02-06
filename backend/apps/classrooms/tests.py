from rest_framework import status
from rest_framework.test import APITestCase

from apps.classrooms.models import Classroom
from apps.users.models import User


class ClassroomAdminManagementTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_classroom',
            password='pass1234',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        self.teacher = User.objects.create_user(username='teacher_classroom', password='pass1234', role='teacher')
        self.student = User.objects.create_user(username='student_classroom', password='pass1234', role='student')
        self.list_url = '/api/classrooms/'

        self.classroom_payload = {
            'name': 'A-301普通教室',
            'building': 'A',
            'floor': 3,
            'room_number': '301',
            'capacity': 80,
            'classroom_type': 'lecture',
            'description': '测试教室',
            'is_available': True,
            'has_projector': True,
            'has_computer': True,
            'has_microphone': False,
            'has_whiteboard': True,
            'has_air_conditioning': True,
        }

    def test_admin_can_create_classroom(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.list_url, self.classroom_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 1)
        self.assertEqual(Classroom.objects.first().name, self.classroom_payload['name'])

    def test_teacher_cannot_create_classroom(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(self.list_url, self.classroom_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Classroom.objects.count(), 0)

    def test_student_cannot_create_classroom(self):
        self.client.force_authenticate(self.student)
        response = self.client.post(self.list_url, self.classroom_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Classroom.objects.count(), 0)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.models import Course
from apps.users.models import User


class CourseApiPermissionTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher_a', password='pass1234', role='teacher')
        self.teacher_other = User.objects.create_user(username='teacher_b', password='pass1234', role='teacher')
        self.student = User.objects.create_user(username='student_a', password='pass1234', role='student')
        self.admin = User.objects.create_user(
            username='admin_a',
            password='pass1234',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )

        self.course_teacher = Course.objects.create(
            name='数学',
            teacher=self.teacher,
            classroom_type='lecture',
            description='数学课程'
        )
        self.course_teacher_other = Course.objects.create(
            name='物理',
            teacher=self.teacher_other,
            classroom_type='lab',
            description='物理课程'
        )

        self.list_url = reverse('course-list')

    def test_teacher_can_only_see_own_courses(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = response.data['results'] if isinstance(response.data, dict) else response.data
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['id'], self.course_teacher.id)

    def test_student_cannot_access_courses_api(self):
        self.client.force_authenticate(self.student)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_cannot_access_courses_api(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_cannot_create_courses_via_api(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            self.list_url,
            {
                'name': '化学',
                'teacher': self.teacher.id,
                'classroom_type': 'lecture',
                'description': '化学课程',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

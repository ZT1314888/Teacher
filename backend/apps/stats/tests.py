from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.classrooms.models import Classroom
from apps.reservations.models import Reservation
from apps.users.models import User


class StatsRoleAccessTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_stats',
            password='pass1234',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        self.teacher = User.objects.create_user(username='teacher_stats', password='pass1234', role='teacher')
        self.student = User.objects.create_user(username='student_stats', password='pass1234', role='student')

        self.classroom = Classroom.objects.create(
            name='C-101普通教室',
            building='C',
            floor=1,
            room_number='101',
            capacity=60,
            classroom_type='lecture',
            is_available=True,
        )

        date = timezone.localdate() + timedelta(days=1)
        Reservation.objects.create(
            classroom=self.classroom,
            user=self.teacher,
            date=date,
            start_time='14:00',
            end_time='16:00',
            purpose='教师预约',
            participant_count=20,
            status='pending',
        )
        Reservation.objects.create(
            classroom=self.classroom,
            user=self.student,
            date=date,
            start_time='16:00',
            end_time='18:00',
            purpose='学生预约',
            participant_count=30,
            status='approved',
        )

    def test_admin_can_export_stats(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get('/api/stats/export/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), 0)
        self.assertIn('rows', response.data.get('data', {}))

    def test_teacher_cannot_export_stats(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.get('/api/stats/export/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('code'), 1)

    def test_dashboard_stats_scope_for_student(self):
        self.client.force_authenticate(self.student)
        response = self.client.get('/api/stats/dashboard/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data.get('data', {})
        self.assertEqual(payload.get('total_reservations'), 1)
        self.assertEqual(payload.get('approved_reservations'), 1)
        self.assertEqual(payload.get('pending_reservations'), 0)

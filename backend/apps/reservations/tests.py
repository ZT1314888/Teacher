from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.classrooms.models import Classroom
from apps.courses.models import Course
from apps.reservations.models import Reservation
from apps.notifications.models import Notification
from apps.users.models import User


class ReservationCourseTypeValidationTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher_course', password='pass1234', role='teacher')
        self.teacher_other = User.objects.create_user(username='teacher_other', password='pass1234', role='teacher')

        self.lecture_room = Classroom.objects.create(
            name='A-101普通教室',
            building='A',
            floor=1,
            room_number='101',
            capacity=60,
            classroom_type='lecture',
            is_available=True,
        )
        self.lab_room = Classroom.objects.create(
            name='B-201实验室',
            building='B',
            floor=2,
            room_number='201',
            capacity=40,
            classroom_type='lab',
            is_available=True,
        )

        self.course_math = Course.objects.create(
            name='数学',
            teacher=self.teacher,
            classroom_type='lecture',
            description='仅普通教室'
        )
        self.course_physics_other = Course.objects.create(
            name='物理',
            teacher=self.teacher_other,
            classroom_type='lab',
            description='仅实验室'
        )

        self.create_url = reverse('reservation-list')
        self.future_date = timezone.localdate() + timedelta(days=1)

    def _payload(self, classroom_id, course_id=None):
        payload = {
            'classroom': classroom_id,
            'date': self.future_date.isoformat(),
            'start_time': '14:00',
            'end_time': '16:00',
            'purpose': '课程教学',
            'description': '课程预约',
            'participant_count': 30,
        }
        if course_id is not None:
            payload['course_id'] = course_id
        return payload

    def test_teacher_can_create_reservation_with_matching_course_type(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            self.create_url,
            self._payload(self.lecture_room.id, course_id=self.course_math.id),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.first().classroom_id, self.lecture_room.id)

    def test_create_reservation_rejects_mismatched_course_classroom_type(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            self.create_url,
            self._payload(self.lab_room.id, course_id=self.course_math.id),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('仅可预约', str(response.data))
        self.assertEqual(Reservation.objects.count(), 0)

    def test_create_reservation_rejects_other_teachers_course_id(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            self.create_url,
            self._payload(self.lab_room.id, course_id=self.course_physics_other.id),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('不属于当前教师', str(response.data))
        self.assertEqual(Reservation.objects.count(), 0)


class ReservationAdminReviewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_review',
            password='pass1234',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        self.teacher = User.objects.create_user(username='teacher_review', password='pass1234', role='teacher')
        self.student = User.objects.create_user(username='student_review', password='pass1234', role='student')

        self.classroom = Classroom.objects.create(
            name='D-101普通教室',
            building='D',
            floor=1,
            room_number='101',
            capacity=80,
            classroom_type='lecture',
            is_available=True,
        )
        self.reservation = Reservation.objects.create(
            classroom=self.classroom,
            user=self.teacher,
            date=timezone.localdate() + timedelta(days=1),
            start_time='14:00',
            end_time='16:00',
            purpose='课程教学',
            participant_count=30,
            status='pending',
        )

    def test_admin_can_approve_reservation(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse('reservation-approve', args=[self.reservation.id]),
            {'comment': '通过'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'approved')
        self.assertEqual(self.reservation.reviewed_by_id, self.admin.id)
        self.assertTrue(
            Notification.objects.filter(
                user=self.teacher,
                type='approval',
            ).exists()
        )

    def test_teacher_cannot_approve_reservation(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            reverse('reservation-approve', args=[self.reservation.id]),
            {'comment': '越权尝试'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'pending')

    def test_student_cannot_reject_reservation(self):
        self.client.force_authenticate(self.student)
        response = self.client.post(
            reverse('reservation-reject', args=[self.reservation.id]),
            {'comment': '越权尝试'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'pending')

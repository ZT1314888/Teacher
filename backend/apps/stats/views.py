from datetime import timedelta
from django.core.cache import cache
from django.db import models
from django.db.models import Count, F
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.classrooms.models import Classroom
from apps.reservations.models import Reservation
from core.responses import ok, fail


def expire_outdated_reservations():
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()
    updated_past = Reservation.objects.filter(
        status__in=['pending', 'approved'],
        date__lt=today
    ).update(status='expired')
    updated_today = Reservation.objects.filter(
        status__in=['pending', 'approved'],
        date=today,
        end_time__lte=current_time
    ).update(status='expired')
    return updated_past + updated_today


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        updated_count = expire_outdated_reservations()
        if updated_count:
            cache.clear()

        today = timezone.localdate().isoformat()
        scope = 'global' if request.user.role == 'admin' else f'user:{request.user.id}'
        cache_key = f'stats:dashboard:{scope}:{today}'
        cached = cache.get(cache_key)
        if cached is not None:
            return ok(cached)

        reservation_queryset = Reservation.objects.all()
        if request.user.role != 'admin':
            reservation_queryset = reservation_queryset.filter(user=request.user)

        data = {
            'total_classrooms': Classroom.objects.count(),
            'available_classrooms': Classroom.objects.filter(is_available=True).count(),
            'total_reservations': reservation_queryset.count(),
            'pending_reservations': reservation_queryset.filter(status='pending').count(),
            'approved_reservations': reservation_queryset.filter(status='approved').count(),
        }
        cache.set(cache_key, data, timeout=300)
        return ok(data)


class ClassroomUsageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        updated_count = expire_outdated_reservations()
        if updated_count:
            cache.clear()

        queryset = Reservation.objects.select_related('classroom')
        if request.user.role != 'admin':
            queryset = queryset.filter(user=request.user)

        # 避免 annotation 名称与 Reservation.classroom_id 冲突，直接使用 values 字段名
        usage_rows = queryset.values(
            'classroom_id',
            'classroom__name'
        ).annotate(
            reservation_count=Count('id')
        ).order_by('-reservation_count')

        data = [
            {
                'classroom_id': row['classroom_id'],
                'classroom_name': row['classroom__name'],
                'reservation_count': row['reservation_count'],
                'hours_used': 0.0,
            }
            for row in usage_rows
        ]
        return ok(data)


class DailySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        updated_count = expire_outdated_reservations()
        if updated_count:
            cache.clear()

        today = timezone.localdate()
        start = today - timedelta(days=6)
        queryset = Reservation.objects.filter(date__range=[start, today])
        if request.user.role != 'admin':
            queryset = queryset.filter(user=request.user)

        rows = queryset.values('date').annotate(
            total=Count('id'),
            approved=Count('id', filter=models.Q(status='approved')),
            rejected=Count('id', filter=models.Q(status='rejected')),
            cancelled=Count('id', filter=models.Q(status='cancelled')),
            expired=Count('id', filter=models.Q(status='expired')),
        ).order_by('date')

        return ok(list(rows))


class ExportStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return fail(message='无权限导出统计数据', status=403)

        rows = Reservation.objects.select_related('classroom', 'user').values(
            'id',
            'date',
            'start_time',
            'end_time',
            'status',
            classroom_name=F('classroom__name'),
            username=F('user__username'),
        ).order_by('-date')[:500]
        return ok({'rows': list(rows)})

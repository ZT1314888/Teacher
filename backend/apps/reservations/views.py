from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Reservation, ReservationStatusLog
from .serializers import ReservationSerializer, ReservationListSerializer
from apps.users.permissions import IsAdminUser
from apps.notifications.models import Notification

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['classroom', 'user', 'date', 'status']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer
        return ReservationSerializer

    def _expire_outdated_reservations(self):
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
        if updated_past or updated_today:
            cache.clear()

    def _invalidate_stats_cache(self, reservation_user_id=None):
        # 统一清理统计缓存，避免后台直接改状态或多角色统计出现旧数据
        cache.clear()
    
    def get_queryset(self):
        self._expire_outdated_reservations()
        user = self.request.user
        if user.role == 'admin':
            return Reservation.objects.select_related('classroom', 'user', 'reviewed_by')
        elif user.role == 'teacher':
            return Reservation.objects.select_related('classroom', 'user', 'reviewed_by').filter(user=user)
        else:  # student
            return Reservation.objects.select_related('classroom', 'user', 'reviewed_by').filter(user=user)

    def perform_create(self, serializer):
        classroom_id = self.request.data.get('classroom')
        date = self.request.data.get('date')
        start_time = self.request.data.get('start_time')
        lock_key = f'reservation:lock:{classroom_id}:{date}:{start_time}'
        lock_ttl = 10
        acquired = cache.add(lock_key, '1', timeout=lock_ttl)
        if not acquired:
            raise ValueError('该时间段预约请求过于频繁，请稍后重试')

        try:
            reservation = serializer.save()
            ReservationStatusLog.objects.create(
                reservation=reservation,
                from_status='',
                to_status=reservation.status,
                operator=self.request.user
            )
            self._invalidate_stats_cache(reservation.user_id)
        finally:
            cache.delete(lock_key)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_409_CONFLICT)
        except (DjangoValidationError, DRFValidationError) as exc:
            detail = getattr(exc, 'message_dict', None) or getattr(exc, 'messages', None) or str(exc)
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def check_conflict(self, request):
        """检查预约冲突"""
        self._expire_outdated_reservations()
        classroom_id = request.data.get('classroom')
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        reservation_id = request.data.get('reservation_id')
        
        if reservation_id:
            conflicting = Reservation.objects.filter(
                classroom_id=classroom_id,
                date=date,
                status__in=['pending', 'approved']
            ).exclude(id=reservation_id)
        else:
            conflicting = Reservation.objects.filter(
                classroom_id=classroom_id,
                date=date,
                status__in=['pending', 'approved']
            )
        
        conflicts = []
        for res in conflicting:
            if (start_time < str(res.end_time) and end_time > str(res.start_time)):
                conflicts.append({
                    'id': res.id,
                    'start_time': res.start_time,
                    'end_time': res.end_time,
                    'user': res.user.username
                })
        
        return Response({
            'has_conflict': len(conflicts) > 0,
            'conflicts': conflicts
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """批准预约"""
        reservation = self.get_object()
        old_status = reservation.status
        reservation.status = 'approved'
        reservation.reviewed_by = request.user
        reservation.review_comment = request.data.get('comment', '')
        reservation.save()
        ReservationStatusLog.objects.create(
            reservation=reservation,
            from_status=old_status,
            to_status='approved',
            operator=request.user
        )
        Notification.objects.create(
            user=reservation.user,
            type='approval',
            content=f'您的预约已通过：{reservation.classroom.name} {reservation.date} {reservation.start_time}-{reservation.end_time}'
        )
        self._invalidate_stats_cache(reservation.user_id)
        return Response({'message': '预约已批准'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """拒绝预约"""
        reservation = self.get_object()
        old_status = reservation.status
        reservation.status = 'rejected'
        reservation.reviewed_by = request.user
        reservation.review_comment = request.data.get('comment', '')
        reservation.save()
        ReservationStatusLog.objects.create(
            reservation=reservation,
            from_status=old_status,
            to_status='rejected',
            operator=request.user
        )
        Notification.objects.create(
            user=reservation.user,
            type='rejection',
            content=f'您的预约被拒绝：{reservation.classroom.name} {reservation.date} {reservation.start_time}-{reservation.end_time}'
        )
        self._invalidate_stats_cache(reservation.user_id)
        return Response({'message': '预约已拒绝'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        reservation = self.get_object()
        if reservation.user != request.user and request.user.role != 'admin':
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        now = timezone.localtime()
        reservation_start = timezone.make_aware(datetime.combine(reservation.date, reservation.start_time))
        if request.user.role != 'admin' and reservation_start - now < timedelta(hours=2):
            return Response({'detail': '开始前2小时内不可取消'}, status=status.HTTP_400_BAD_REQUEST)

        old_status = reservation.status
        reservation.status = 'cancelled'
        reservation.save()
        ReservationStatusLog.objects.create(
            reservation=reservation,
            from_status=old_status,
            to_status='cancelled',
            operator=request.user
        )
        Notification.objects.create(
            user=reservation.user,
            type='cancel',
            content=f'预约已取消：{reservation.classroom.name} {reservation.date} {reservation.start_time}-{reservation.end_time}'
        )
        self._invalidate_stats_cache(reservation.user_id)
        return Response({'message': '预约已取消'})
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """获取我的预约"""
        self._expire_outdated_reservations()
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)

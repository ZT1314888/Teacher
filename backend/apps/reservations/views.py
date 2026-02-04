from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime
from .models import Reservation
from .serializers import ReservationSerializer, ReservationListSerializer
from apps.users.permissions import IsAdminUser, IsTeacherOrAdmin

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['classroom', 'user', 'date', 'status']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer
        return ReservationSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Reservation.objects.all()
        elif user.role == 'teacher':
            return Reservation.objects.filter(user=user)
        else:  # student
            return Reservation.objects.filter(user=user)
    
    @action(detail=False, methods=['post'])
    def check_conflict(self, request):
        """检查预约冲突"""
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
        reservation.status = 'approved'
        reservation.reviewed_by = request.user
        reservation.review_comment = request.data.get('comment', '')
        reservation.save()
        return Response({'message': '预约已批准'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """拒绝预约"""
        reservation = self.get_object()
        reservation.status = 'rejected'
        reservation.reviewed_by = request.user
        reservation.review_comment = request.data.get('comment', '')
        reservation.save()
        return Response({'message': '预约已拒绝'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        reservation = self.get_object()
        if reservation.user != request.user and request.user.role != 'admin':
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'message': '预约已取消'})
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """获取我的预约"""
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)

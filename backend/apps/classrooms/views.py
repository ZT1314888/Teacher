from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from apps.reservations.models import Reservation
from .models import Classroom
from .serializers import ClassroomSerializer, ClassroomListSerializer
from apps.users.permissions import IsAdminUser

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['classroom_type', 'building', 'is_available']
    search_fields = ['name', 'building', 'room_number']
    ordering_fields = ['capacity', 'building', 'floor']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClassroomListSerializer
        return ClassroomSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """获取可用教室列表"""
        classrooms = self.queryset.filter(is_available=True)
        serializer = ClassroomListSerializer(classrooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def recommend(self, request):
        """规则型推荐：容量匹配 + 设备匹配 + 历史使用率 + 时间冲突校验"""
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        participant_count = int(request.data.get('participant_count') or 0)
        classroom_type = request.data.get('classroom_type')
        requirements = request.data.get('requirements') or {}

        if not date or not start_time or not end_time:
            return Response({'detail': 'date/start_time/end_time are required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Classroom.objects.filter(is_available=True)
        if classroom_type:
            queryset = queryset.filter(classroom_type=classroom_type)
        if participant_count > 0:
            queryset = queryset.filter(capacity__gte=participant_count)

        equipment_fields = ['has_projector', 'has_computer', 'has_microphone', 'has_whiteboard', 'has_air_conditioning']
        for field in equipment_fields:
            if requirements.get(field) is True:
                queryset = queryset.filter(**{field: True})

        conflict_classroom_ids = set(
            Reservation.objects.filter(
                date=date,
                status__in=['pending', 'approved'],
                start_time__lt=end_time,
                end_time__gt=start_time
            ).values_list('classroom_id', flat=True)
        )

        candidates = [room for room in queryset if room.id not in conflict_classroom_ids]
        if not candidates:
            return Response({'recommendations': []})

        room_ids = [room.id for room in candidates]
        usage_map = {
            item['classroom_id']: item['count']
            for item in Reservation.objects.filter(
                classroom_id__in=room_ids,
                status='approved'
            ).values('classroom_id').annotate(count=Count('id'))
        }

        def score(room):
            capacity_gap = max((room.capacity or 0) - participant_count, 0)
            usage = usage_map.get(room.id, 0)
            # 优先容量贴合，同时考虑历史使用率（避免过度集中）
            return (capacity_gap, usage, room.id)

        candidates.sort(key=score)
        serializer = ClassroomListSerializer(candidates[:5], many=True)
        return Response({'recommendations': serializer.data})

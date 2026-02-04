from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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

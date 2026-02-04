from rest_framework import serializers
from .models import Classroom

class ClassroomSerializer(serializers.ModelSerializer):
    classroom_type_display = serializers.CharField(source='get_classroom_type_display', read_only=True)
    
    class Meta:
        model = Classroom
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ClassroomListSerializer(serializers.ModelSerializer):
    classroom_type_display = serializers.CharField(source='get_classroom_type_display', read_only=True)
    
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'building', 'floor', 'room_number', 'capacity', 
                  'classroom_type', 'classroom_type_display', 'is_available',
                  'has_projector', 'has_computer', 'has_microphone', 
                  'has_whiteboard', 'has_air_conditioning']

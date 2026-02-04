from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)
    classroom_type_display = serializers.CharField(source='get_classroom_type_display', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'teacher', 'teacher_name',
            'classroom_type', 'classroom_type_display',
            'description', 'created_at'
        ]
        read_only_fields = ['teacher', 'created_at']

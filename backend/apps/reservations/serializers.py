from rest_framework import serializers
from .models import Reservation
from apps.classrooms.serializers import ClassroomListSerializer
from apps.users.serializers import UserSerializer
from apps.courses.models import Course

class ReservationSerializer(serializers.ModelSerializer):
    classroom_detail = ClassroomListSerializer(source='classroom', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    course_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['user', 'status', 'reviewed_by', 'review_comment', 'created_at', 'updated_at']
    
    def validate(self, data):
        # 验证时间逻辑
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('结束时间必须晚于开始时间')
        
        # 验证人数
        if data['participant_count'] > data['classroom'].capacity:
            raise serializers.ValidationError(f'参与人数不能超过教室容量({data["classroom"].capacity}人)')

        # 课程预约场景校验：课程必须属于当前教师，且教室类型必须匹配课程限制
        course_id = data.get('course_id')
        if course_id is not None:
            request = self.context.get('request')
            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated or user.role != 'teacher':
                raise serializers.ValidationError('仅教师可按课程进行预约')

            course = Course.objects.filter(id=course_id, teacher=user).first()
            if not course:
                raise serializers.ValidationError('课程不存在或不属于当前教师')

            if data['classroom'].classroom_type != course.classroom_type:
                raise serializers.ValidationError(
                    f'该课程仅可预约{course.get_classroom_type_display()}'
                )
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('course_id', None)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReservationListSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'classroom', 'classroom_name', 'user', 'user_name', 'date',
                  'start_time', 'end_time', 'purpose', 'description', 'participant_count',
                  'status', 'status_display', 'created_at']

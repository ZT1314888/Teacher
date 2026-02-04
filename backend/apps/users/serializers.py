from rest_framework import serializers
from .models import User, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                  'phone', 'department', 'department_name', 'is_backend_registered', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_backend_registered']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 
                  'last_name', 'role', 'phone', 'department']
    
    def validate_username(self, value):
        # 用户名唯一性校验
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已存在')
        return value

    def validate_email(self, value):
        # 邮箱唯一性校验
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已注册')
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("密码不匹配")
        # 前端注册不允许注册管理员
        if data.get('role') == 'admin':
            raise serializers.ValidationError("不能通过前端注册管理员账号")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['is_backend_registered'] = False
        # 确保非管理员不能访问后台
        validated_data['is_staff'] = False
        user = User.objects.create_user(**validated_data)
        return user




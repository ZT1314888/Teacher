from rest_framework import serializers
from django.conf import settings
from .models import Announcement
import re

class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    content = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'author', 'author_name', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_content(self, obj):
        """将相对路径的图片和视频转换为完整URL"""
        content = obj.content
        request = self.context.get('request')
        
        if request:
            # 获取基础URL
            base_url = request.build_absolute_uri('/')[:-1]
            
            # 替换图片路径
            content = re.sub(
                r'src="(/media/[^"]+)"',
                f'src="{base_url}\\1"',
                content
            )
            
            # 替换视频路径
            content = re.sub(
                r'src="(/media/[^"]+)"',
                f'src="{base_url}\\1"',
                content
            )
        
        return content


class AnnouncementListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'author_name', 'created_at']

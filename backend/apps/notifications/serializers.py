from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    announcement_id = serializers.IntegerField(source='announcement.id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'type', 'type_display', 'content', 'is_read', 'created_at', 'announcement_id']

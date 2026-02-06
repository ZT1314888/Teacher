from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = (
        ('approval', '审批通过'),
        ('rejection', '审批拒绝'),
        ('reminder', '提醒'),
        ('cancel', '取消'),
        ('system', '系统'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    announcement = models.ForeignKey(
        'announcements.Announcement',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user_id}:{self.type}:{self.content[:20]}'

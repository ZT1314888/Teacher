from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from apps.users.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements', verbose_name='发布人')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'announcements'
        verbose_name = '公告'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

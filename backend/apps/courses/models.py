from django.db import models
from apps.users.models import User
from apps.classrooms.models import Classroom

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='课程名称')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='授课教师')
    classroom_type = models.CharField(max_length=20, choices=Classroom.CLASSROOM_TYPE_CHOICES, verbose_name='适用教室类型')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

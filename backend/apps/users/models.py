from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name='角色')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='院系')
    is_backend_registered = models.BooleanField(default=False, verbose_name='后端注册')
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # 确保只有管理员才能访问后台
        if self.role == 'admin':
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='院系名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='院系代码')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'departments'
        verbose_name = '院系'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name




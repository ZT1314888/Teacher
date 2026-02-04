from django.db import models

class Classroom(models.Model):
    CLASSROOM_TYPE_CHOICES = (
        ('lecture', '普通教室'),
        ('lab', '实验室'),
        ('multimedia', '多媒体教室'),
        ('conference', '会议室'),
        ('art', '艺术室'),
    )
    
    name = models.CharField(max_length=50, unique=True, verbose_name='教室名称')
    building = models.CharField(max_length=50, verbose_name='楼栋')
    floor = models.IntegerField(verbose_name='楼层')
    room_number = models.CharField(max_length=20, verbose_name='房间号')
    capacity = models.IntegerField(verbose_name='容量')
    classroom_type = models.CharField(max_length=20, choices=CLASSROOM_TYPE_CHOICES, verbose_name='教室类型')
    
    # 设备配置
    has_projector = models.BooleanField(default=False, verbose_name='投影仪')
    has_computer = models.BooleanField(default=False, verbose_name='电脑')
    has_microphone = models.BooleanField(default=False, verbose_name='麦克风')
    has_whiteboard = models.BooleanField(default=False, verbose_name='白板')
    has_air_conditioning = models.BooleanField(default=False, verbose_name='空调')
    
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'classrooms'
        verbose_name = '教室'
        verbose_name_plural = verbose_name
        ordering = ['building', 'floor', 'room_number']

    def __str__(self):
        return f"{self.building}-{self.room_number} ({self.name})"

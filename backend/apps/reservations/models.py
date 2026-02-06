from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.users.models import User
from apps.classrooms.models import Classroom

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('cancelled', '已取消'),
        ('expired', '已过期'),
    )
    
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='reservations', verbose_name='教室')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='预约人')
    
    date = models.DateField(verbose_name='预约日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    
    purpose = models.CharField(max_length=200, verbose_name='使用目的')
    description = models.TextField(blank=True, null=True, verbose_name='详细说明')
    participant_count = models.IntegerField(verbose_name='参与人数')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='reviewed_reservations', verbose_name='审核人')
    review_comment = models.TextField(blank=True, null=True, verbose_name='审核意见')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'reservations'
        verbose_name = '预约'
        verbose_name_plural = verbose_name
        ordering = ['-date', '-start_time']
        indexes = [
            models.Index(fields=['date', 'status']),
            models.Index(fields=['user', 'date']),
            models.Index(fields=['classroom', 'date']),
        ]

    def __str__(self):
        return f"{self.classroom.name} - {self.date} {self.start_time}-{self.end_time}"
    
    def clean(self):
        # 验证时间逻辑
        if self.start_time >= self.end_time:
            raise ValidationError('结束时间必须晚于开始时间')

        # 验证预约时间是否早于当前时间（使用本地时区）
        now = timezone.localtime()
        current_time = now.time().replace(tzinfo=None)
        # 如果预约日期早于今天，视为失效
        if self.date < now.date():
            raise ValidationError('预约日期不能早于今天')
        # 如果是今天，仅当该时间段已结束才禁止
        elif self.date == now.date() and self.end_time <= current_time:
            raise ValidationError('预约时间段已结束，请选择未来的时间段')
        
        # 验证人数不超过教室容量
        if self.participant_count > self.classroom.capacity:
            raise ValidationError(f'参与人数不能超过教室容量({self.classroom.capacity}人)')
        
        # 检查时间冲突
        if self.pk:
            conflicting = Reservation.objects.filter(
                classroom=self.classroom,
                date=self.date,
                status__in=['pending', 'approved']
            ).exclude(pk=self.pk)
        else:
            conflicting = Reservation.objects.filter(
                classroom=self.classroom,
                date=self.date,
                status__in=['pending', 'approved']
            )
        
        for reservation in conflicting:
            if (self.start_time < reservation.end_time and self.end_time > reservation.start_time):
                raise ValidationError(f'该时间段与现有预约冲突: {reservation.start_time}-{reservation.end_time}')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ReservationStatusLog(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='status_logs')
    from_status = models.CharField(max_length=20, blank=True, null=True)
    to_status = models.CharField(max_length=20)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservation_status_logs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservation_status_logs'
        ordering = ['-created_at']

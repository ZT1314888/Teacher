from django.db import models


class ClassroomUsageStats(models.Model):
    classroom = models.ForeignKey('classrooms.Classroom', on_delete=models.CASCADE, related_name='usage_stats')
    date = models.DateField()
    hours_used = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    reservation_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'classroom_usage_stats'
        unique_together = [('classroom', 'date')]


class DailyReservationSummary(models.Model):
    date = models.DateField(unique=True)
    total_reservations = models.IntegerField(default=0)
    approved_count = models.IntegerField(default=0)
    rejected_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'daily_reservation_summary'

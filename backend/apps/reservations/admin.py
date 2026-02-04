from django.contrib import admin
from django.utils.html import format_html
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'user', 'date', 'start_time', 'end_time', 'status_icon', 'created_at']
    list_filter = ['status', 'date', 'classroom']
    search_fields = ['user__username', 'classroom__name', 'purpose']
    date_hierarchy = 'date'

    @admin.display(description='状态', ordering='status')
    def status_icon(self, obj):
        """在后台列表中用彩色圆点显示预约状态"""
        if obj.status == 'approved':
            color = '#22c55e'  # 绿色
        elif obj.status in ['rejected', 'pending']:
            color = '#ef4444'  # 红色（拒绝、待审核）
        else:
            color = '#9ca3af'  # 灰色（待审核、已取消等）

        label = obj.get_status_display()
        return format_html(
            '<span style="display:inline-flex;align-items:center;gap:6px;">'
            '<span style="width:10px;height:10px;border-radius:50%;background:{};display:inline-block;"></span>'
            '{}</span>',
            color,
            label,
        )

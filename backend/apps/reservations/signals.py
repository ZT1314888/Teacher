from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Reservation


@receiver(post_save, sender=Reservation)
def invalidate_stats_cache_on_reservation_save(sender, instance, **kwargs):
    # 任意预约变更（创建、审批、拒绝、取消、后台编辑）后立即清理统计缓存
    cache.clear()


@receiver(post_delete, sender=Reservation)
def invalidate_stats_cache_on_reservation_delete(sender, instance, **kwargs):
    cache.clear()

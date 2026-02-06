from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Classroom


@receiver(post_save, sender=Classroom)
def invalidate_stats_cache_on_classroom_save(sender, instance, **kwargs):
    # 教室可用性、容量、类型等变更会影响统计报表，统一失效缓存
    cache.clear()


@receiver(post_delete, sender=Classroom)
def invalidate_stats_cache_on_classroom_delete(sender, instance, **kwargs):
    cache.clear()

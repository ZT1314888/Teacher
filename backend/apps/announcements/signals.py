from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.notifications.models import Notification
from apps.users.models import User

from .models import Announcement


@receiver(pre_save, sender=Announcement)
def remember_previous_publish_state(sender, instance, **kwargs):
    if not instance.pk:
        instance._published_before = False
        return
    instance._published_before = (
        Announcement.objects.filter(pk=instance.pk).values_list('is_published', flat=True).first() or False
    )


@receiver(post_save, sender=Announcement)
def create_announcement_notifications(sender, instance, created, **kwargs):
    published_before = getattr(instance, '_published_before', False)
    just_published = created and instance.is_published
    switched_to_published = (not created) and instance.is_published and (not published_before)

    if not (just_published or switched_to_published):
        return

    # 防止重复写入同一公告通知
    if Notification.objects.filter(announcement=instance).exists():
        return

    recipients = User.objects.filter(is_active=True)
    rows = [
        Notification(
            user=user,
            announcement=instance,
            type='system',
            content=f'系统发布了新公告：《{instance.title}》'
        )
        for user in recipients
    ]
    if rows:
        Notification.objects.bulk_create(rows, batch_size=500)

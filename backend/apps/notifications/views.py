from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        notification_id = request.data.get('id')
        if not notification_id:
            return Response({'detail': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)

        obj = self.get_queryset().filter(id=notification_id).first()
        if not obj:
            return Response({'detail': 'notification not found'}, status=status.HTTP_404_NOT_FOUND)

        obj.is_read = True
        obj.save(update_fields=['is_read'])
        return Response({'message': 'ok'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'message': 'ok'})

    @action(detail=False, methods=['post'])
    def mark_announcement_read(self, request):
        announcement_id = request.data.get('announcement_id')
        if not announcement_id:
            return Response({'detail': 'announcement_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        obj = self.get_queryset().filter(
            announcement_id=announcement_id,
            is_read=False
        ).order_by('created_at').first()

        if obj:
            obj.is_read = True
            obj.save(update_fields=['is_read'])

        return Response({'message': 'ok'})

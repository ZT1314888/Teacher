from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from apps.users.permissions import IsTeacherUser

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherUser]
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

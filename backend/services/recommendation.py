from apps.classrooms.models import Classroom


def recommend_classrooms(classroom_type=None, participant_count=0, requirements=None):
    requirements = requirements or {}
    queryset = Classroom.objects.filter(is_available=True)
    if classroom_type:
        queryset = queryset.filter(classroom_type=classroom_type)
    if participant_count:
        queryset = queryset.filter(capacity__gte=participant_count)

    for field in ['has_projector', 'has_computer', 'has_microphone', 'has_whiteboard', 'has_air_conditioning']:
        if requirements.get(field) is True:
            queryset = queryset.filter(**{field: True})

    return queryset.order_by('capacity')

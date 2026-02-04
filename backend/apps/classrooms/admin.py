from django.contrib import admin
from .models import Classroom

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'floor', 'room_number', 'capacity', 'classroom_type', 'is_available']
    list_filter = ['classroom_type', 'building', 'is_available']
    search_fields = ['name', 'building', 'room_number']
    list_editable = ['is_available']

    class Media:
        css = {
            'all': ('classrooms/admin.css',)
        }
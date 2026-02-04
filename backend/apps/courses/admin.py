from django.contrib import admin
from .models import Course
from apps.users.models import User

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'classroom_type', 'created_at']
    list_filter = ['classroom_type', 'created_at']
    search_fields = ['name', 'teacher__username']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['queryset'] = User.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

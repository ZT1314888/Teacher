from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    total_classrooms = serializers.IntegerField()
    available_classrooms = serializers.IntegerField()
    total_reservations = serializers.IntegerField()
    pending_reservations = serializers.IntegerField()
    approved_reservations = serializers.IntegerField()


class ClassroomUsageSerializer(serializers.Serializer):
    classroom_id = serializers.IntegerField()
    classroom_name = serializers.CharField()
    reservation_count = serializers.IntegerField()
    hours_used = serializers.FloatField()


class DailySummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    total = serializers.IntegerField()
    approved = serializers.IntegerField()
    rejected = serializers.IntegerField()
    cancelled = serializers.IntegerField()

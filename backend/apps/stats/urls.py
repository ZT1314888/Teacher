from django.urls import path
from .views import DashboardStatsView, ClassroomUsageView, DailySummaryView, ExportStatsView

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view()),
    path('classroom-usage/', ClassroomUsageView.as_view()),
    path('daily-summary/', DailySummaryView.as_view()),
    path('export/', ExportStatsView.as_view()),
]

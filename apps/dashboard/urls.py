from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='dashboard_home'),
    path('videos/', views.VideoManageView.as_view(), name='dashboard_videos'),
    path('import/trigger/', views.trigger_import, name='dashboard_trigger_import'),
]

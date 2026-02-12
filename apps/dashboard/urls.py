from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='dashboard_home'),
    
    # Video URLs
    path('videos/', views.VideoManageView.as_view(), name='dashboard_videos'),
    path('videos/add/', views.VideoCreateView.as_view(), name='dashboard_video_add'),
    path('videos/<uuid:pk>/edit/', views.VideoUpdateView.as_view(), name='dashboard_video_edit'),
    path('videos/<uuid:pk>/delete/', views.VideoDeleteView.as_view(), name='dashboard_video_delete'),
    
    # Category URLs
    path('categories/', views.CategoryManageView.as_view(), name='dashboard_categories'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='dashboard_category_add'),
    path('categories/<uuid:pk>/edit/', views.CategoryUpdateView.as_view(), name='dashboard_category_edit'),
    path('categories/<uuid:pk>/delete/', views.CategoryDeleteView.as_view(), name='dashboard_category_delete'),
    
    # Actions
    path('import/trigger/', views.trigger_import, name='dashboard_trigger_import'),
]

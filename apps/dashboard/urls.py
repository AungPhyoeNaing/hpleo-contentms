from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.DashboardLoginView.as_view(), name='dashboard_login'),
    path('logout/', views.DashboardLogoutView.as_view(), name='dashboard_logout'),

    path('', views.DashboardHomeView.as_view(), name='dashboard_home'),
    
    # Resource URLs
    path('resources/', views.ResourceManageView.as_view(), name='dashboard_resources'),
    path('resources/add/', views.ResourceCreateView.as_view(), name='dashboard_resource_add'),
    path('resources/<uuid:pk>/edit/', views.ResourceUpdateView.as_view(), name='dashboard_resource_edit'),
    path('resources/<uuid:pk>/delete/', views.ResourceDeleteView.as_view(), name='dashboard_resource_delete'),
    
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

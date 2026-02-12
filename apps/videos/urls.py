from django.urls import path
from .views import VideoListView, VideoDetailView, CategoryVideoListView

urlpatterns = [
    path('', VideoListView.as_view(), name='home'),
    path('video/<uuid:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('category/<uuid:category_id>/', CategoryVideoListView.as_view(), name='category_list'),
]

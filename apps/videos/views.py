from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Video, Category, Episode

class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category').order_by('-updated_at')
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        return context

class CategoryVideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 24

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Video.objects.filter(category=self.category).select_related('category').order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        context['categories'] = Category.objects.all().order_by('name')
        return context

class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get episodes
        episodes = self.object.episodes.all().order_by('index')
        context['episodes'] = episodes
        
        # Determine current episode
        episode_id = self.request.GET.get('ep')
        if episode_id:
            current_episode = episodes.filter(id=episode_id).first()
        else:
            current_episode = episodes.first()
            
        context['current_episode'] = current_episode
        
        # Related videos (same category)
        if self.object.category:
            context['related_videos'] = Video.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id).order_by('?')[:6]
            
        return context

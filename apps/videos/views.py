from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from .models import Video, Category, Episode

class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 24

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['videos/partials/video_loop.html']
        return [self.template_name]

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
        
        # Featured Video (Random highly viewed or latest)
        # Optimization: Try to get one with a thumbnail
        if not self.request.headers.get('HX-Request'):
             context['featured_video'] = Video.objects.filter(
                 thumbnail_url__isnull=False
             ).order_by('-created_at').first()
             
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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Atomically increment views count
        Video.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        # Refresh from db to get the updated value
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get episodes
        episodes = self.object.episodes.all().order_by('index')
        context['episodes'] = episodes
        
        # Determine current episode
        episode_id = self.request.GET.get('ep')
        current_episode = None
        
        if episode_id:
            try:
                current_episode = episodes.filter(id=episode_id).first()
            except ValueError: # Handle invalid UUID strings
                pass
        
        if not current_episode:
            current_episode = episodes.first()
            
        context['current_episode'] = current_episode
        
        # Related videos (Optimized)
        if self.object.category:
            # Get up to 100 IDs from the same category to sample from
            related_ids = list(Video.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id).values_list('id', flat=True)[:100])
            
            import random
            if len(related_ids) > 6:
                sampled_ids = random.sample(related_ids, 6)
                context['related_videos'] = Video.objects.filter(id__in=sampled_ids)
            else:
                context['related_videos'] = Video.objects.filter(id__in=related_ids)
            
        return context

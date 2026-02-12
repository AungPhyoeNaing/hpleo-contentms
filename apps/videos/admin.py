from django.contrib import admin
from .models import Video, Category, Episode

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title',)
    inlines = [EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('video', 'label', 'index', 'url')
    list_filter = ('video',)

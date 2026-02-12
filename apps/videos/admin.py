from django.contrib import admin
from .models import Video, Category, Episode

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0
    ordering = ('index',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'id')
    search_fields = ('name',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'external_id', 'created_at')
    search_fields = ('title', 'external_id')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'views')
    inlines = [EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('video', 'label', 'index', 'url')
    search_fields = ('video__title', 'label')
    list_filter = ('video__category',)

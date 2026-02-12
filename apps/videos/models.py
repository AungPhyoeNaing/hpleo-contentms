from django.db import models
import uuid

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    # external_id might be needed if categories map 1:1, but the prompt says "type_name -> Category.name"
    # and "Auto-create category if missing". So we might just match by name.
    # However, keeping external_id is safer if provided (type_id).
    external_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    thumbnail_url = models.URLField(max_length=1000, blank=True, null=True) # Increased length just in case
    description = models.TextField(blank=True)
    external_id = models.IntegerField(unique=True, help_text="vod_id from external API")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Episode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='episodes')
    label = models.CharField(max_length=100)
    url = models.URLField(max_length=1000)
    index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"{self.video.title} - {self.label}"

from django.db import models
import uuid

class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="e.g. Caobizy, 188Resource")
    url = models.URLField(help_text="The API URL (e.g. https://www.caobizy.com/api.php/provide/vod/)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ImportLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    success_count = models.PositiveIntegerField(default=0)
    fail_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, default='pending') # pending, running, completed, failed
    details = models.TextField(blank=True, null=True) # JSON or text log of errors

    def __str__(self):
        return f"Import {self.started_at} - {self.status}"

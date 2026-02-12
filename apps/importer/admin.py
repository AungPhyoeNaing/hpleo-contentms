from django.contrib import admin
from .models import ImportLog

@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ('started_at', 'status', 'success_count', 'fail_count')
    list_filter = ('status',)

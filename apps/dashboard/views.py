from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from asgiref.sync import async_to_sync
from apps.videos.models import Video, Category
from apps.importer.models import ImportLog
from apps.importer.services import CaobizyImporter

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DashboardHomeView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_videos'] = Video.objects.count()
        context['total_categories'] = Category.objects.count()
        context['recent_logs'] = ImportLog.objects.order_by('-started_at')[:5]
        context['last_success'] = ImportLog.objects.filter(status='completed').order_by('-finished_at').first()
        return context

class VideoManageView(StaffRequiredMixin, ListView):
    model = Video
    template_name = 'dashboard/videos.html'
    context_object_name = 'videos'
    paginate_by = 50
    ordering = '-updated_at'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

@require_POST
def trigger_import(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    # Get pages from POST data, default to 1
    try:
        pages = int(request.POST.get('pages', 1))
    except ValueError:
        pages = 1

    # Run import synchronously (Note: heavy imports might timeout without Celery)
    importer = CaobizyImporter()
    try:
        log = async_to_sync(importer.run_import)(pages=pages)
        status_color = "text-green-500" if log.status == 'completed' else "text-red-500"
        return HttpResponse(
            f"<span class='{status_color} font-bold'>Done! Scanned {pages} page(s). Added: {log.success_count}</span>"
        )
    except Exception as e:
        return HttpResponse(f"<span class='text-red-500'>Error: {str(e)}</span>")

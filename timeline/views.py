from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView

from blog.models import SubscribeRecord, SubscribeByBlog
from core.libs import LoginUrlMixin
from timeline.models import Timeline


class DetailTimelineView(LoginRequiredMixin, LoginUrlMixin, DetailView):
    template_name = 'timeline/index.html'
    queryset = Timeline.objects.all()

    def get(self, request, *args, **kwargs):
        timeline = self.get_object()
        subscribes_by_blog = SubscribeByBlog.objects.filter(timeline=timeline)
        subscribes_record = []
        for subscribe_by_blog in subscribes_by_blog:
            subscribes_record.extend(subscribe_by_blog.subscribes_record.all())
        paginator = Paginator(subscribes_record, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'timeline': timeline, 'page_obj': page_obj})

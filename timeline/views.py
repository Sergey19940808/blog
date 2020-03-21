from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from blog.models import SubscribeRecord, SubscribeByBlog
from core.libs import LoginUrlMixin
from timeline.libs import GetSubscribeRecordIdsMixin
from timeline.models import Timeline


class DetailTimelineView(
    LoginRequiredMixin,
    LoginUrlMixin,
    GetSubscribeRecordIdsMixin,
    DetailView
):
    template_name = 'timeline/index.html'
    queryset = Timeline.objects.all()

    def get(self, request, *args, **kwargs):
        timeline = self.get_object()

        subscribes_by_blog = SubscribeByBlog.objects.filter(timeline=timeline)
        subscribes_record_ids = self.get_subscribes_record_ids(subscribes_by_blog)
        subscribes_record = SubscribeRecord.objects.filter(
            id__in=subscribes_record_ids
        ).order_by('-record__created_at')

        paginator = Paginator(subscribes_record, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'timeline': timeline, 'page_obj': page_obj})


class MarkAsReadView(
    LoginRequiredMixin,
    LoginUrlMixin,
    View
):
    def dispatch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        subscribe_record = SubscribeRecord.objects.get(id=kwargs.get('id'))
        subscribe_record.is_read = True
        subscribe_record.save()
        return redirect(reverse('timeline:index_timeline', kwargs={'pk': kwargs.get('pk')}))

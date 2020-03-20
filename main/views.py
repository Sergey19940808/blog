from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from blog.models import Blog
from core.libs import LoginUrlMixin
from timeline.models import Timeline


class MainView(LoginRequiredMixin, LoginUrlMixin, TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(user=request.user)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        user = kwargs.get('user')
        context.update({
            'blog': Blog.objects.filter(user=user).first(),
            'timeline': Timeline.objects.filter(user=user).first(),
        })
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from blog.models import Blog


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_anonymous:
            return redirect('users/login')
        else:
            context = self.get_context_data(user=request.user)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        user = kwargs.get('user')
        context.update({'blog': Blog.objects.filter(user=user).first()})
        return context

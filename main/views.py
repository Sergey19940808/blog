from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_anonymous:
            return redirect('users/login')
        else:
            return render(request, self.template_name)

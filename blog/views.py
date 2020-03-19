from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, FormView
from django.core.paginator import Paginator

from blog.forms import RecordForm
from blog.models import Blog, Record


class DetailBlogView(LoginRequiredMixin, DetailView):
    template_name = 'blog/index.html'
    queryset = Blog.objects.all()

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        records = Record.objects.filter(blog=blog)
        paginator = Paginator(records, 1)
        page_number = request.GET.get('page')
        records_part = paginator.get_page(page_number)
        return render(request, self.template_name, {'blog': blog, 'records': records_part})


class CreateRecordView(LoginRequiredMixin, FormView):
    template_name = 'blog/create_record.html'
    form_class = RecordForm
    blog = None

    def get(self, request, *args, **kwargs):
        self.get_blog(request)
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        form = self.form_class
        return {
            'form': form,
            'blog': self.blog
        }

    def post(self, request, *args, **kwargs):
        self.get_blog(request)
        self.success_url = reverse('blog:index', kwargs={'pk': self.blog.id})
        return super(CreateRecordView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        record.blog = self.blog
        record.save()
        return super(CreateRecordView, self).form_valid(form)

    def get_blog(self, request):
        self.blog = Blog.objects.filter(user=request.user).first()


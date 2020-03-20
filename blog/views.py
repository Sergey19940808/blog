from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView, CreateView
from django.core.paginator import Paginator

from blog.forms import RecordForm
from blog.libs import GetBlogMixin, SubscribeByBlogMixin, BaseDispatchPostMixin
from blog.models import Blog, Record, SubscribeByBlog
from core.libs import LoginUrlMixin


# Blog Part
class DetailBlogView(LoginRequiredMixin, LoginUrlMixin, DetailView):
    template_name = 'blog/index.html'
    queryset = Blog.objects.all()

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        records = Record.objects.filter(blog=blog)
        paginator = Paginator(records, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'blog': blog, 'page_obj': page_obj})


class ListOtherBlogView(
    LoginRequiredMixin,
    LoginUrlMixin,
    SubscribeByBlogMixin,
    GetBlogMixin,
    ListView
):
    template_name = 'blog/list_other.html'
    queryset = Blog.objects.all()

    def get(self, request, *args, **kwargs):
        my_blog = self.get_blog(request)
        other_blogs = Blog.objects.all().exclude(id=my_blog.id)
        other_blogs = self.get_is_subscribe(other_blogs, request.user)
        paginator = Paginator(other_blogs, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})


# Record Part
class CreateRecordView(LoginRequiredMixin, LoginUrlMixin, GetBlogMixin, FormView):
    template_name = 'blog/create_record.html'
    form_class = RecordForm
    blog = None

    def get(self, request, *args, **kwargs):
        self.blog = self.get_blog(request)
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        form = self.form_class
        return {
            'form': form,
            'blog': self.blog
        }

    def post(self, request, *args, **kwargs):
        self.blog = self.get_blog(request)
        self.success_url = reverse('blog:index', kwargs={'pk': self.blog.id})
        return super(CreateRecordView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        record.blog = self.blog
        record.save()
        return super(CreateRecordView, self).form_valid(form)


# Subscribe by blog Part
class CreateSubscribeByBlogView(BaseDispatchPostMixin, View):
    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs.get("pk"))
        user = request.user
        subscribe_by_blog = SubscribeByBlog.objects.create(user=user)
        blog.subscribes_by_blog.add(subscribe_by_blog)
        return redirect('blog:other_blogs')


class DeleteSubscribeByBlogView(BaseDispatchPostMixin, CreateView):
    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs.get("pk"))
        user = request.user
        subscribe_by_blog = blog.subscribes_by_blog.filter(user=user)
        subscribe_by_blog.delete()
        return redirect('blog:other_blogs')


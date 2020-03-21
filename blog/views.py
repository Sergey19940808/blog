from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView, CreateView
from django.core.paginator import Paginator

from blog.forms import RecordForm
from blog.libs import GetBlogMixin, SubscribeByBlogMixin
from blog.models import Blog, Record, SubscribeByBlog, SubscribeRecord
from core.libs import LoginUrlMixin
from timeline.models import Timeline


# Blog Part
class DetailBlogView(LoginRequiredMixin, LoginUrlMixin, DetailView):
    template_name = 'blog/index_blog.html'
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
    template_name = 'blog/list_other_blog.html'
    queryset = Blog.objects.all()
    paginate_by = 15
    object_list = None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(user=request.user)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self, **kwargs):
        user = kwargs.get('user')
        my_blog = self.get_blog(user)
        other_blogs = Blog.objects.all().exclude(id=my_blog.id)
        return self.get_is_subscribe(other_blogs, user)


# Record Part
class CreateRecordView(LoginRequiredMixin, LoginUrlMixin, GetBlogMixin, FormView):
    template_name = 'blog/create_record.html'
    form_class = RecordForm
    blog = None

    def get(self, request, *args, **kwargs):
        self.blog = self.get_blog(request.user)
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        form = self.form_class
        return {
            'form': form,
            'blog': self.blog
        }

    def post(self, request, *args, **kwargs):
        self.blog = self.get_blog(request.user)
        self.success_url = reverse('blog:index_blog', kwargs={'pk': self.blog.id})
        return super(CreateRecordView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        record.blog = self.blog
        record.save()
        return super(CreateRecordView, self).form_valid(form)


class DetailRecordView(LoginRequiredMixin, LoginUrlMixin, DetailView):
    template_name = 'blog/index_record.html'
    queryset = Record.objects.all()

    def get(self, request, *args, **kwargs):
        blog = Blog.objects.filter(id=kwargs.get('pk')).first()
        record = Record.objects.filter(blog=blog, id=kwargs.get('id')).first()
        return render(request, self.template_name, {'record': record})


# Subscribe Part
class CreateSubscribeByBlogView(View):
    def dispatch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs.get("pk"))
        timeline = Timeline.objects.get(user=request.user)
        subscribe_by_blog = SubscribeByBlog.objects.create(timeline=timeline)
        subscribe_by_blog.subscribes_record.add(
            *[SubscribeRecord.objects.create(record=record) for record in blog.record_set.all()]
        )
        blog.subscribes_by_blog.add(subscribe_by_blog)
        return redirect('blog:list_other_blogs')


class DeleteSubscribeByBlogView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs.get("pk"))
        user = request.user
        subscribe_by_blog = blog.subscribes_by_blog.filter(user=user).first()
        subscribe_by_blog.subscribes_record.all().delete()
        subscribe_by_blog.delete()
        return redirect('blog:list_other_blogs')


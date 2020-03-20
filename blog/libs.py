from blog.models import Blog


class GetBlogMixin:
    def get_blog(self, request):
        return Blog.objects.filter(user=request.user).first()


class SubscribeByBlogMixin:
    def get_is_subscribe(self, other_blogs, current_user):
        for other_blog in other_blogs:
            other_blog.is_subscribe = True if other_blog.subscribe_by_blog(current_user) else False
        return other_blogs
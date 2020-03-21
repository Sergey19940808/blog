from blog.models import Blog


class GetBlogMixin:
    def get_blog(self, current_user):
        return Blog.objects.filter(user=current_user).first()


class SubscribeByBlogMixin:
    def get_is_subscribe(self, other_blogs, current_user):
        for other_blog in other_blogs:
            other_blog.is_subscribe = True if self._subscribe_by_blog(other_blog, current_user) else False
        return other_blogs

    def _subscribe_by_blog(self, blog, current_user):
        return blog.subscribes_by_blog.filter(timeline__user=current_user).first()
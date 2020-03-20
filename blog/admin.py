from django.contrib import admin

from blog.models import Blog, Record, SubscribeByBlog

admin.site.register(Blog)
admin.site.register(Record)
admin.site.register(SubscribeByBlog)

from django.urls import path
from blog.views import (
    ListOtherBlogView,
    DetailBlogView,
    CreateRecordView,
    DetailRecordView,
    CreateSubscribeByBlogView,
    DeleteSubscribeByBlogView,
)

urlpatterns = [
    path('other_blogs', ListOtherBlogView.as_view(), name='list_other_blogs'),
    path('<int:pk>', DetailBlogView.as_view(), name='index_blog'),
    path('<int:pk>/record/create', CreateRecordView.as_view(), name='create_record'),
    path('<int:pk>/record/<int:id>', DetailRecordView.as_view(), name='index_record'),
    path('<int:pk>/subscribe_by_blog/create', CreateSubscribeByBlogView.as_view(), name='create_subscribe_by_blog'),
    path('<int:pk>/subscribe_by_blog/delete', DeleteSubscribeByBlogView.as_view(), name='delete_subscribe_by_blog'),
]
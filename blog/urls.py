from django.urls import path
from blog.views import DetailBlogView, CreateRecordView

urlpatterns = [
    path('<int:pk>', DetailBlogView.as_view(), name='index'),
    path('<int:pk>/record/create', CreateRecordView.as_view(), name='create_record'),
]
from django.urls import path

from timeline.views import DetailTimelineView, MarkAsReadView
urlpatterns = [
    path('<int:pk>', DetailTimelineView.as_view(), name='index'),
    path('<int:pk>/subscribe_record/<int:id>', MarkAsReadView.as_view(), name='mark_as_read'),
]
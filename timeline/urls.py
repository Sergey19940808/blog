from django.urls import path

from timeline.views import DetailTimelineView
urlpatterns = [
    path('<int:pk>', DetailTimelineView.as_view(), name='index')
]
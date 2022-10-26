from django.urls import path
from .views import *

urlpatterns = [
    path("create/", WordCreateView.as_view(), name="word-create"),
    path("<str:username>/<slug:slug>/", WordDetailView.as_view(), name="word-detail"),
    path("", MyWordsListView.as_view(), name="word-list"),
    path("upload-video/", VideoUploadView.as_view(), name="upload-video"),
    path("video/<str:username>/<slug:slug>/", VideoUploadDetailView.as_view(), name="video-detail"),
    path("videos/", MyVideoListView.as_view(), name="video-list"),
]

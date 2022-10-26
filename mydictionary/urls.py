from django.urls import path
from .views import *

urlpatterns = [
    path("word/create/", WordCreateView.as_view(), name="word-create"),
    path("word/<str:username>/<slug:slug>/", WordDetailView.as_view(), name="word-detail"),
    path("words", MyWordsListView.as_view(), name="word-list"),
    path("video/upload/", VideoUploadView.as_view(), name="upload-video"),
    path("video/<str:username>/<slug:slug>/", VideoUploadDetailView.as_view(), name="video-detail"),
    path("videos/", MyVideoListView.as_view(), name="video-list"),
    path("video-category/create/", VideoCategoryCreate.as_view(), name="videocategory-create"),
    path("video-category/<str:username>/<slug:slug>/", VideoCategoryDetail.as_view(), name="word-detail"),
]

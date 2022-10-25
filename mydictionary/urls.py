from django.urls import path
from .views import *

urlpatterns = [
    path("create/", WordCreateView.as_view(), name="word-create"),
    path("<str:username>/<slug:slug>/", WordDetailView.as_view(), name="word-detail"),
    path("", MyWordsListView.as_view(), name="word-list"),
]

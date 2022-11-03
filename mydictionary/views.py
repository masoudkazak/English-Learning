from .models import *
from .permissions import IsOwnerOrSuperuser
from .tasks import create_word_task, upload_video_task
from .serializers import *

from rest_framework.views import APIView
from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.core.files import File

import csv
import codecs


class WordCreateView(APIView):
    serializer_class = WordCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordDetailView(APIView):
    serializer_class = WordCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def get_object(self):
        word = get_object_or_404(Word, 
            owner__username=self.kwargs["username"],
            slug=self.kwargs["slug"]
            )
        return word

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        word = self.get_object()
        word.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyWordsListView(ListAPIView):
    serializer_class = WordCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', "translate"]
    ordering_fields = ['name', "status", "updated"]

    def get_queryset(self):
        words = Word.objects.filter(owner=self.request.user)
        return words


class CSVWordsUploadView(APIView):
    serializer_class = WordsCSVFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]
            csvfile = csv.reader(codecs.iterdecode(file, "utf-8"))
            for row in csvfile:
                create_word_task.delay(
                    row[0],
                    row[1],
                    request.user.id,
                )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUploadView(APIView):
    serializer_class = VideoUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]

            storage = FileSystemStorage()
            storage.save(
                file.name,
                File(file)
            )
            upload_video_task.delay(
                serializer.validated_data["title"],
                storage.path(file.name),
                request.user.id,
                file.name,
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUploadDetailView(APIView):
    serializer_class = VideoDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def get_object(self):
        video = get_object_or_404(Video, 
            slug=self.kwargs["slug"],
            owner__username=self.kwargs["username"]
            )
        return video
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, requset, *args, **kwargs):
        video = self.get_object()
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyVideoListView(ListAPIView):
    serializer_class = VideoUploadSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']

    def get_queryset(self):
        videos = Video.objects.filter(owner=self.request.user)
        return videos

from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class WordCreateView(APIView):
    serializer_class = WordCreateSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordDetailView(APIView):
    serializer_class = WordCreateSerializer

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        word = self.get_object()
        word.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyWordsListView(APIView):
    serializer_class = WordCreateSerializer

    def get_queryset(self):
        words = Word.objects.filter(owner=self.request.user)
        return words

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoUploadView(APIView):
    serializer_class = VideoUploadSerializer
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoUploadDetailView(APIView):
    serializer_class = VideoUploadSerializer

    def get_object(self):
        video = get_object_or_404(Video, 
            slug=self.kwargs["slug"],
            owner__username=self.kwargs["username"]
            )
        return video
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, requset, *args, **kwargs):
        video = self.get_object()
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyVideoListView(APIView):
    serializer_class = VideoUploadSerializer

    def get_queryset(self):
        videos = Video.objects.filter(owner=self.request.user)
        return videos

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoCategoryCreate(APIView):
    serializer_class = VideoCategorySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoCategoryDetail(APIView):
    serializer_class = VideoCategorySerializer

    def get_object(self):
        category = get_object_or_404(VideoCategory, 
            slug=self.kwargs["slug"],
            owner__username=self.kwargs["username"]
            )
        return category
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, requset, *args, **kwargs):
        video = self.get_object()
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import serializers
from .models import *


class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        exclude = ("slug", "created", "updated")
        

class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        exclude = ("slug",)    


class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ("slug",)

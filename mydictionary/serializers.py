from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import csv
import codecs

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
    

class WordsCSVFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(["csv"])],
        )

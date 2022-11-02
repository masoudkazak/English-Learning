from rest_framework import serializers
from .models import *
from django.core.validators import FileExtensionValidator


class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        exclude = ("slug", "created", "updated")
        

class VideoUploadSerializer(serializers.Serializer):
    title = serializers.CharField()
    file = serializers.FileField(
        validators=[FileExtensionValidator(["mp4"])],
        )


class VideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ("slug",)


class WordsCSVFileSerializer(serializers.Serializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(["csv"])],
        )

from rest_framework import serializers
from .models import *


class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        exclude = ("slug", "created", "updated")
        

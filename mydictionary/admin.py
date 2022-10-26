from django.contrib import admin
from .models import *


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(VideoCategory)
class VideCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

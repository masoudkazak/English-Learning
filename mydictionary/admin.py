from django.contrib import admin
from .models import *


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ["name", "translate", "owner"]
    search_fields = ["name", "translate"]
    list_filter = ["status"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(VideoCategory)
class VideCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "owner"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}

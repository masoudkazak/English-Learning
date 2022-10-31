from enum import unique
from django.db import models
from slugify import slugify
from django.contrib.auth.models import User


class Word(models.Model):    
    class Status(models.IntegerChoices):
        weak = 0
        normal = 1
        good = 2
        
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    translate = models.CharField(max_length=50)
    pronunciation = models.CharField(max_length=50, blank=True, null=True)
    example = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "words"
        verbose_name = "word"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class VideoCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"
        verbose_name = "category"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.ManyToManyField(VideoCategory, blank=True, null=True)
    file = models.FileField(upload_to="%Y/%m/%d/")
    words = models.ManyToManyField(Word, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "videos"
        verbose_name = "video"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models
from slugify import slugify
from django.contrib.auth.models import User


class Word(models.Model):
    class Type(models.IntegerChoices):
        Noun = 0
        Verb = 1
    
    class Status(models.IntegerChoices):
        weak = 0
        normal = 1
        good = 2
        
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    translate = models.CharField(max_length=50)
    pronounciation = models.CharField(max_length=50, blank=True, null=True)
    example = models.TextField(blank=True, null=True)
    type_word = models.CharField(choices=Type.choices, max_length=1)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=Status.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "words"
        verbose_name = "word"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField()
    words = models.ManyToManyField(Word)

    def __str__(self):
        return self.title

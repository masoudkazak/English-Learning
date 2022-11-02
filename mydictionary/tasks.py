from celery import shared_task
from .models import Word, Video
from django.contrib.auth.models import User


@shared_task()
def create_word_task(name, translate, id):
    owner = User.objects.get(id=id)
    Word.objects.create(
        name=name,
        translate=translate,
        owner=owner,
    )


@shared_task()
def upload_video_task(data):
    Video.objects.create(data)
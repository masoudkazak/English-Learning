from celery import shared_task
from .models import Word, Video
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from pathlib import Path


@shared_task()
def create_word_task(name, translate, id):
    print("Uploading Words File...")
    owner = User.objects.get(id=id)
    Word.objects.create(
        name=name,
        translate=translate,
        owner=owner,
    )
    print("Uploaded")


@shared_task()
def upload_video_task(title, path, id, file_name):
    print("Uploading Video...")
    owner = User.objects.get(id=id)
    storage = FileSystemStorage()
    path_object = Path(path)

    with path_object.open(mode="rb") as file:
        video = File(file, name=path_object.name)

        Video.objects.create(
            title=title,
            file=video,
            owner=owner,
        )
    storage.delete(file_name)
    print("Uploaded")

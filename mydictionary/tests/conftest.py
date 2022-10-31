import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from mydictionary.models import VideoCategory, Word
import random


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_create_fixture():
    user = User.objects.create_user(
        username="someone1",
        password="something"
        )
    return user


@pytest.fixture
def word_create_fixture():
    user = User.objects.create_user(
        username="someone1",
        password="something"
        )
    word = Word.objects.create(
        name ="Hello my friend",
        owner =user,
        translate ="سلام دوست من",
        pronunciation ="hello/mai/frend",
        example =" adsdasd asdaad asdsa",
        description ="dasds dad saad sa dasd sad",
        status =random.randint(0,2),
    )
    return word


@pytest.fixture
def video_category_create_fixture():
    user = User.objects.create_user(
        username="someone1",
        password="something"
        )
    category = VideoCategory.objects.create(
        name ="My Course",
        owner =user,
    )
    return category
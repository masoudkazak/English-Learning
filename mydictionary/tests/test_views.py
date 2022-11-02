from time import sleep
import pytest
from rest_framework import status
from django.urls import reverse
import random
from mydictionary.models import Video, Word


pytestmark = pytest.mark.django_db


def test_create_word_HTTP_201(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)

    word_create = {
        "name":"Hi Guys",
        "owner":user_create_fixture.id,
        "translate":"سلام داداشیا", 
        "pronunciation":"hai/gaiz", 
        "example":"Hi guys, How are you?",
        "description":"abcdefg hijk lmnop", 
        "status":random.randint(0, 2),
    }

    response = api_client.post(reverse("mydictionary:word-create"), word_create)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_word_set_bad_status(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)

    word_create = {
        "name":"Hi Guys",
        "owner":user_create_fixture.id,
        "translate":"سلام داداشیا", 
        "pronunciation":"hai/gaiz", 
        "example":"Hi guys, How are you?",
        "description":"abcdefg hijk lmnop", 
        "status":3, #must be between 0 and 2
    }

    response = api_client.post(reverse("mydictionary:word-create"), word_create)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_word_detail_put_delete(api_client, word_create_fixture):
    api_client.force_authenticate(user=word_create_fixture.owner)

    word_update = {
        "name":"Hello my enemy",
        "owner":word_create_fixture.owner.id,
        "translate":"سلام دشمن", 
        "pronunciation":"hello/my/enemy", 
        "example":"Hello my enemy, How are you?",
        "description":"abcdefg hijk lmnop", 
        "status":random.randint(0, 2), #must be between 0 and 2  
    }

    response_put = api_client.put(reverse("mydictionary:word-detail",
                                    kwargs={"username":word_create_fixture.owner.username,
                                            "slug":word_create_fixture.slug}),
                                 word_update)

    assert Word.objects.filter(
        owner=word_create_fixture.owner,
        name="Hello my enemy",
    ).exists()

    response_delete = api_client.delete(reverse("mydictionary:word-detail",
                                            kwargs={"username":word_create_fixture.owner.username,
                                                    "slug":"hello-my-enemy"}))
    
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    

# How can we know that this page has objects?
def test_mywords_http_200(api_client, word_create_fixture):
    api_client.force_authenticate(user=word_create_fixture.owner)

    response = api_client.get(reverse("mydictionary:word-list"))

    assert response.status_code == status.HTTP_200_OK


def test_video_upload_HTTP_201(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)

    with open("/home/masoud/Desktop/sample.mp4", "rb") as file:
        print(file)
        video_create = {
            "title":"welcome",
            "file":file,
            "owner":user_create_fixture.id
        }
        response = api_client.post(reverse("mydictionary:upload-video"), video_create)
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_video_delete(api_client, video_upload_fixture):
    api_client.force_authenticate(user=video_upload_fixture.owner)

    response_delete = api_client.delete(reverse("mydictionary:video-detail",
                                            kwargs={
                                                "username":video_upload_fixture.owner.username,
                                                "slug":video_upload_fixture.slug,
                                            }))                                  
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT


def test_video_list_http_200(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    
    response = api_client.get(reverse("mydictionary:video-list"))

    assert response.status_code == status.HTTP_200_OK


def test_csv_upload_words_create(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)

    with open("/home/masoud/Desktop/sample2.csv", "rb") as file:
        csv_create = {
            "file":file,
        }
        response = api_client.post(reverse("mydictionary:word-csv"), csv_create)
    assert response.status_code == status.HTTP_202_ACCEPTED

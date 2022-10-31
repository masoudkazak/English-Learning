import pytest
from rest_framework import status
from django.urls import reverse
import random
from mydictionary.models import VideoCategory, Word


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
# def test_mywords_http_200(api_client, word_create_fixture):
#     api_client.force_authenticate(user=word_create_fixture.owner)

#     response = api_client.get(reverse("mydictionary:word-list"))

#     assert response.status_code == status.HTTP_200_OK


# def test_video_upload_HTTP_201(api_client, user_create_fixture):
#     api_client.force_authenticate(user=user_create_fixture)

#     video_create = {
#         "title":"welcome",
#         "file":"/media/test/9af5a68a7cbe7b93606cd31835cb13cf48401502-144p_RSxgeDT.mp4",
#         "owner":user_create_fixture.id
#     }
#     response = api_client.post(reverse("mydictionary:upload-video"), video_create)

#     assert response.status_code == status.HTTP_201_CREATED


# Here test VideoUploadDetailView


# Here test VideoUploadListView


def test_video_category_create_http_200(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)

    category = {
        "name":"Course",
        "owner":user_create_fixture.id,
    }
    response = api_client.post(reverse("mydictionary:videocategory-create"), category)

    assert response.status_code == status.HTTP_201_CREATED


def test_video_category_put_delete(api_client, video_category_create_fixture):
    api_client.force_authenticate(user=video_category_create_fixture.owner)

    category_update = {
        "name":"His Course",
        "owner":video_category_create_fixture.owner.id,
    }

    response_put = api_client.put(reverse("mydictionary:videocategory-detail",
                                    kwargs={
                                        "username":video_category_create_fixture.owner.username,
                                        "slug":video_category_create_fixture.slug,
                                    }),
                                    category_update)
    new_category = VideoCategory.objects.filter(owner=video_category_create_fixture.owner.id)[0]
    assert new_category.name != video_category_create_fixture.name

    response_delete = api_client.delete(reverse("mydictionary:videocategory-detail",
                                            kwargs={
                                                "username":new_category.owner.username,
                                                "slug":new_category.slug,
                                            }))
    print(VideoCategory.objects.filter(owner=video_category_create_fixture.owner.id))
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
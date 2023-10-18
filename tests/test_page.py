import pytest
from rest_framework import status


@pytest.mark.urls("innoter_project.innoter_project.urls")
class TestPage:
    pytestmark = pytest.mark.django_db

    def test_create_page(self, client, generate_fake_token, generate_random_page_info):
        token = generate_fake_token
        data = generate_random_page_info
        resp = client.post(
            "/page/", headers={"Authorization": "Bearer {}".format(token)}, data=data
        )
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        assert data_from_resp["name"] == data["name"]
        assert data_from_resp["description"] == data["description"]

    def test_delete_page(
        self,
        client,
        generate_fake_token,
        generate_random_page_info,
        disable_pageviewset_permissions,
    ):
        token = generate_fake_token
        data = generate_random_page_info
        resp = client.post(
            "/page/", headers={"Authorization": "Bearer {}".format(token)}, data=data
        )
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        delete_resp = client.delete(
            f"/page/{data_from_resp['id']}/",
            headers={"Authorization": "Bearer {}".format(token)},
        )
        assert delete_resp.status_code == status.HTTP_200_OK

    def test_patch_page(self, client, generate_fake_token, generate_random_page_info):
        token = generate_fake_token
        data = generate_random_page_info
        resp = client.post(
            "/page/", headers={"Authorization": "Bearer {}".format(token)}, data=data
        )
        data_for_patch = {
            "description": "updated_description",
        }
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        patch_resp = client.patch(
            f"/page/{data_from_resp['id']}/",
            headers={"Authorization": "Bearer {}".format(token)},
            data=data_for_patch,
        )
        assert patch_resp.status_code == status.HTTP_200_OK
        data_from_patch_resp = patch_resp.json()
        assert data_from_patch_resp["name"] == data["name"]
        assert data_from_patch_resp["description"] == data_for_patch["description"]

    def test_follow_and_unfollow_page(
        self, client, generate_fake_token, generate_random_page_info
    ):
        token = generate_fake_token
        data = generate_random_page_info
        resp = client.post(
            "/page/", headers={"Authorization": "Bearer {}".format(token)}, data=data
        )
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        follow_page = client.patch(
            f"/page/{data_from_resp['id']}/follow/",
            headers={"Authorization": "Bearer {}".format(token)},
        )
        follow_data_from_resp = follow_page.json()
        assert follow_page.status_code == status.HTTP_201_CREATED
        assert follow_data_from_resp["message"] == "Followed"

        unfollow_page = client.patch(
            f"/page/{data_from_resp['id']}/unfollow/",
            headers={"Authorization": "Bearer {}".format(token)},
        )
        unfollow_data_from_resp = unfollow_page.json()
        assert unfollow_page.status_code == status.HTTP_201_CREATED
        assert unfollow_data_from_resp["message"] == "Unfollowed"

    def test_create_post(
        self,
        client,
        generate_fake_token,
        generate_random_page_info,
        generate_random_post_info,
    ):
        token = generate_fake_token
        data = generate_random_page_info
        post_info = generate_random_post_info
        resp = client.post(
            "/page/", headers={"Authorization": "Bearer {}".format(token)}, data=data
        )
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        post_resp = client.post(
            f"/page/{data_from_resp['id']}/post/",
            headers={"Authorization": "Bearer {}".format(token)},
            data=post_info,
        )
        data_from_post_resp = post_resp.json()
        assert post_resp.status_code == status.HTTP_201_CREATED
        assert data_from_post_resp["page"] == data_from_resp["name"]
        assert data_from_post_resp["content"] == post_info["content"]
        assert data_from_post_resp["reply_to"] is None
        assert data_from_post_resp["likes"] == []

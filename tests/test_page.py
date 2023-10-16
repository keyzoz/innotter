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

    def test_delete_page(self, client, generate_fake_token, generate_random_page_info):
        token = generate_fake_token
        data = generate_random_page_info
        resp = client.post(
            "/page/", headers={"Authorization": "Bearer {}".format(token)}, data=data
        )
        assert token is not None
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        assert data_from_resp["name"] == data["name"]
        assert data_from_resp["description"] == data["description"]
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
            "name": "updated_name",
        }
        assert resp.status_code == status.HTTP_201_CREATED
        data_from_resp = resp.json()
        assert data_from_resp["name"] == data["name"]
        assert data_from_resp["description"] == data["description"]
        patch_resp = client.patch(
            f"/page/{data_from_resp['id']}/",
            headers={"Authorization": "Bearer {}".format(token)},
            data=data_for_patch,
        )
        assert patch_resp.status_code == status.HTTP_200_OK
        data_from_patch_resp = patch_resp.json()
        assert data_from_patch_resp["name"] == data_for_patch["name"]
        assert data_from_resp["description"] == data["description"]

import pytest
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.urls("innoter_project.innoter_project.urls")
def test_create_tag(client, generate_fake_token, generate_random_tag_info):
    token = generate_fake_token
    data = generate_random_tag_info
    resp = client.post(
        "/tag/", headers={"Authorization": "Bearer {}".format(token)}, data=data
    )
    assert resp.status_code == status.HTTP_201_CREATED
    data_from_resp = resp.json()
    assert data_from_resp["name"] == data["name"]

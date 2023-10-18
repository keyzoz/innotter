import datetime

import jwt
import psycopg2
import pytest
from django.core.management import call_command
from django.db import connections
from faker import Faker
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from rest_framework.test import APIClient

from innoter_project.innoter_project.settings import JWT_SECRET_KEY

fake = Faker()


def run_sql(sql):
    conn = psycopg2.connect(database="postgres", host="localhost", port="5430")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    from django.conf import settings

    test_db = "db"
    settings.DATABASES["test"]["NAME"] = test_db

    run_sql(f"DROP DATABASE IF EXISTS {test_db}")
    run_sql(f"CREATE DATABASE {test_db}")
    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")
    yield
    for connection in connections.all():
        connection.close()

    run_sql(f"DROP DATABASE {test_db}")


@pytest.fixture
def generate_fake_token():
    payload = {
        "sub": "daasf",
        "type": "access",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "user_id": "59739137-6af7-4d66-98f7-ae67a2dfad25",
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

    return token


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(scope="function")
def generate_random_page_info():

    return {"name": fake.word(), "description": fake.text()}


@pytest.fixture(scope="function")
def generate_random_post_info():

    return {"content": fake.text()}


@pytest.fixture(scope="function")
def generate_random_tag_info():

    return {"name": fake.word()}


@pytest.fixture
def disable_pageviewset_permissions():
    from rest_framework.permissions import AllowAny

    from innoter_project.page.views import PageViewSet

    original_permission_classes = PageViewSet.permission_classes
    PageViewSet.permission_classes = [AllowAny]

    yield

    PageViewSet.permission_classes = original_permission_classes

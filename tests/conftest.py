import datetime

import jwt
import psycopg2
import pytest
from django.conf import settings
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(database="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings

    settings.DATABASES["default"]["NAME"] = "the_copied_db"

    run_sql("DROP DATABASE IF EXISTS the_copied_db")
    run_sql("CREATE DATABASE the_copied_db TEMPLATE the_source_db")

    yield

    for connection in connections.all():
        connection.close()

    run_sql("DROP DATABASE the_copied_db")


@pytest.fixture
def generate_fake_token():
    payload = {
        "sub": "daasf",
        "type": "access",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    return token

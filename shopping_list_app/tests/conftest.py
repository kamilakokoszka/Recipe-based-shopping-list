import os
import sys

import pytest
from django.contrib.auth.models import User
from django.test import Client

from shopping_list_app.tests.utils import create_fake_shopping_list

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User(username='Superadmin')
    user.set_password("123password")
    user.save()
    return user


@pytest.fixture
def set_up():
    create_fake_shopping_list()

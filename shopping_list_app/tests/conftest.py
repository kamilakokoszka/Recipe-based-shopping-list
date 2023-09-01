import os
import sys

import pytest
from django.contrib.auth.models import User
from django.test import Client

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

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from utils.factories import *


# @pytest.fixture
# def user() -> User:
#     return UserFactory()

# @pytest.fixture
# def api_client_jwt_auth(user: get_user_model()):
#     # user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
#     client = APIClient()
#     refresh = RefreshToken.for_user(user)
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
#
#     return client


@pytest.fixture
def user():
    def make_user(**kwargs) -> get_user_model():
        return UserFactory(**kwargs)

    return make_user


@pytest.fixture
def teacher() -> get_user_model():
    return UserFactory(is_teacher=True)


@pytest.fixture
def student() -> get_user_model():
    return UserFactory(is_teacher=False)


@pytest.fixture
def api_client_jwt_auth():
    def jwt_auth(user: get_user_model()):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    return jwt_auth

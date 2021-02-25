from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


# @pytest.fixture
# def user() -> User:
#     return UserFactory()

def get_api_client_jwt_auth(user: get_user_model()):
    # user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client

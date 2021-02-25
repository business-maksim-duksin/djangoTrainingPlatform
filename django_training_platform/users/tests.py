import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_detail(user, api_client_jwt_auth):
    user = user(is_teacher=True)
    client = api_client_jwt_auth(user)
    url = reverse('v1:users:user-detail', kwargs={'pk': user.pk})
    response = client.get(url)
    print(response.__dict__)

    assert response.status_code == 200
    assert user.username in response.content.decode()

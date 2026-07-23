# posts/test_api_pytest.py
import pytest
from django.contrib.auth.models import User
from rest_framework import status
from .models import Post
from rest_framework_simplejwt.tokens import AccessToken



@pytest.fixture
def test_user():
    """Test ushın paydalanıwshı jaratatuǵın fixture."""
    return User.objects.create_user(username='pytestuser', password='pytestpassword')


@pytest.fixture
def test_post(test_user):
    """Test ushın post jaratatuǵın fixture (test_user fixture-ine baylanıslı)."""
    return Post.objects.create(
		    author=test_user, 
		    title='Pytest Test Ataması', 
		    content='Pytest Test Mazmunı'
    )

# Testlerdiń `APITestCase`-den miyras alıwı shárt emes
# `pytest.mark.django_db` dekoratorı test ushın bazanı aktivlestiredi

@pytest.mark.django_db
def test_list_posts(client, test_post):
    """Postlar dizimi durıs qaytıp atırǵanın tekseriw."""
    response = client.get('/api/v1/posts/') 

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    # assert response.data['results'][0]['title'] == 'Pytest Test Ataması'

@pytest.mark.django_db
def test_create_post_auth(client, test_user):
    """Sistemaǵa kirgen paydalanıwshı post jarata alıwın tekseriw."""

    token = AccessToken.for_user(test_user)
    data = {'title': 'Pytest Jańa post', 'content': 'Pytest Jańa mazmun'}
    response = client.post('api/v1/posts/', data,  HTTP_AUTHORIZATION = f'Bearer {token}')

    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1 # Tek usı test ushın baza bos boladı
    assert Post.objects.first().title == 'Pytest Jańa post'
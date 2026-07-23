from django.test import TestCase

# Create your tests here.
# posts/tests.py
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post

class PostApiTests(APITestCase):
    def setUp(self):
        """
        Hár bir test metodı iske túspesten aldın orınlanatuǵın tayarlıq jumısları.
        """
        self.user = User.objects.create_user(
		        username='testuser', 
		        password='testpassword'
        )

        self.post = Post.objects.create(
            author=self.user,
            title='Test ataması',
            content='Test mazmunı'
        )

    # ------ Model Testi ------
    def test_model_str_representation(self):
        """Modeldiń __str__ metodı durıs islep atırǵanın tekseriw."""
        self.assertEqual(str(self.post), 'Test ataması')

    # ------ API Endpoint Testleri ------
    def test_list_posts_unauthenticated(self):
        """Autentifikaciyadan ótpegen paydalanıwshı ushın postlar dizimin tekseriw."""
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # self.assertEqual(response.data['results'][0]['title'], 'Test ataması')


    def test_create_post_authenticated(self):
        """Autentifikaciyadan ótken paydalanıwshı jańa post jarata alıwın tekseriw."""
        # Test ushın sistemaǵa kirgizemiz
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Jańa post', 'content': 'Jańa mazmun'}
        response = self.client.post('/api/v1/posts/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, 'Jańa post')


    def test_create_post_unauthenticated(self):
        """Autentifikaciyadan ótpegen paydalanıwshı post jarata almawın tekseriw."""
        # Bul test ushın sistemaǵa kirmeymiz

        data = {'title': 'Ruqsatsız post', 'content': 'Ruqsatsız mazmun'}
        response = self.client.post('/api/v1/posts/', data)

        # IsAuthenticatedOrReadOnly ruqsatına muwapıq, 401 Unauthorized ornına 403 Forbidden bolıwı múmkin
        # JWT qollanǵanda, token joq bolsa 401 Unauthorized boladı.
        self.assertIn(
		        response.status_code, 
		        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
		    )

    def test_update_post_by_author(self):
        """Post avtorı onı ózgerte alıwın tekseriw."""
        self.client.force_authenticate(user=self.user)

        updated_data = {'title': 'Jańalanǵan atama', 'content': 'Jańalanǵan mazmun'}
        response = self.client.put(f'/api/v1/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db() # Obyektti bazadan jańalap alamız
        self.assertEqual(self.post.title, 'Jańalanǵan atama')

    def test_update_post_by_another_user(self):
        """Basqa paydalanıwshı posttı ózgerte almawın tekseriw (IsAuthorOrReadOnly)."""
        another_user = User.objects.create_user(
		        username='anotheruser', 
		        password='anotherpassword'
        )
        self.client.force_authenticate(user=another_user)

        updated_data = {'title': 'Urlanıwshı atama'}
        response = self.client.put(f'/api/v1/posts/{self.post.id}/', updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
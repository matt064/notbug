from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import BlogPost

class BlogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testMat', password='password')
        self.post = BlogPost.objects.create(title='Test Title', content='test test test', author=self.user)

    
    def test_register_user(self):
        "sing up test"
        response = self.client.post(reverse('blog:registration'), {
            'username': 'newuser',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123'
        })

        # if response.status_code == 200:
        #     print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())  
    

    def test_login_user(self):
        "login test"
        response = self.client.post(reverse('blog:login'), {
            'username': 'testMat',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.wsgi_request.user.is_authenticated) 


    def test_logout_user(self):
        "logout test"
        self.client.login(username='testMat', password='password')
        response = self.client.get(reverse('blog:logout'))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(response.wsgi_request.user.is_authenticated) 


    def test_create_post(self):
        "create new post by user"
        self.client.login(username='testMat', password='password')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'Test Post',
            'content': 'Test Content'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(BlogPost.objects.filter(title='Test Post').exists())  


    def test_update_post(self):
        "edit post by user"
        self.client.login(username='testMat', password='password')
        response = self.client.post(reverse('blog:post_update', args=[self.post.pk]), {
            'title': 'Updated Test Post',
            'content': 'Updated Test Content'
        })
        self.assertEqual(response.status_code, 302) 
        self.post.refresh_from_db() 
        self.assertEqual(self.post.title, 'Updated Test Post')  


    def test_update_post_by_non_author(self):
        "edit post by non author"
        other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='other_user', password='password123')
        response = self.client.post(reverse('blog:post_update', args=[self.post.pk]), {
            'title': 'Invalid Update',
            'content': 'This should not work'
        })
        self.assertEqual(response.status_code, 302) 
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, 'Invalid Update')
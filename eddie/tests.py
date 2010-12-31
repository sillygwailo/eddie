
from django.test import TestCase
from django.test.client import Client

class ViewTest(TestCase):
  fixtures = ['eddie.json',]
  def setUp(self):
    self.client = Client()
  def test_register_page(self):
    data = {
      'username': 'test_user',
      'email': 'test_user@example.com',
      'password1': 'pass123',
      'password2': 'pass123',
    }
    response = self.client.post('/register/', data)
    self.assertRedirects(response, '/register/success/')
  def test_action_save(self):
    data = {
      'username': 'test_user',
      'email': 'test_user@example.com',
      'password1': 'pass123',
      'password2': 'pass123',
    }
    response = self.client.post('/register/', data)
    self.assertRedirects(response, '/register/success/')
    
    response = self.client.login(
      username='test_user',
      password='pass123',
    ) 
    self.assertTrue(response)
    
    data = {
      'title': 'Test Action',
    }
    response = self.client.post('/save/', data)
    self.assertRedirects(response, '/user/test_user/')
    
    response = self.client.get('/user/test_user/')
    self.assertContains(response, 'Test Action')

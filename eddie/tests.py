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
  def test_delete_instance(self):
    test_username = 'test_user'
    test_email = 'test_user@example.com'
    test_password1 = 'pass123'
    test_password2 = 'pass123'
    data = {
      'username': test_username,
      'email': test_email,
      'password1': test_password1,
      'password2': test_password2,
    }
    response = self.client.post('/register/', data)

    response = self.client.login(
      username='test_user',
      password='pass123',
    ) 
    self.assertTrue(response)
    # at this point the test user can create an action and instance, but cannot 
    # delete it. That is, it does not have permission to delete.
    data = {
      'title': 'Test Action',
    }
    response = self.client.post('/save/', data)
    self.assertRedirects(response, '/user/test_user/')
    
    response = self.client.get('/delete/1/')
    self.assertRedirects(response, '/login/?next=/delete/1/')
    
#    user = User.objects.get(username='test_user')
#    user.user_permissions.add('eddie.delete_actioninstance')
    
#    data = {
#      'post': 'yes'
#    }
#    response = self.client.post('/delete/1/')
#    self.assertRedirects(response, '/login/')    
    
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

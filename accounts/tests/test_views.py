from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model, SESSION_KEY
from django.http import HttpRequest
from accounts.views import persona_login

User = get_user_model()  # Find project's user model for use in ORM api


class LoginViewTest(TestCase):
    

    @patch('accounts.views.authenticate')  # 1
    def test_calls_authenticate_with_assertion_from_post(
        self, mock_authenticate  # 2
    ):
        '''
        1: @patch is passed the function we want to mock up so that a real auth request does
        not get sent every time we do a test. 
        2: The auth object is called mock_authenticate.
        3: Making sure mocked object is configurable
        4: Post request with specific data is sent to relevant url
        5: Testing that the mocked object was used instead of true obect by creating
        post request with specific data and validating the data
        '''
        mock_authenticate.return_value = None  # 3
        self.client.post('/accounts/login', {'assertion': 'assert this'}) #4
        mock_authenticate.assert_called_once_with(assertion='assert this') #5 
        

    @patch('accounts.views.authenticate') 
    def test_returns_OK_when_user_found(
        self, mock_authenticate
    ):
        '''
        1: Instance of user in model created
        2: Since we are testing a return value, make sure relevant attribute is set appropirately
        3: Send a post request to url that calls login view function with specific data
        4: Validate decoded data that view function did its job 
        '''
        user = User.objects.create(email = 'a@b.com') # 1
        user.backend = '' # Just requirement for auth_login()
        mock_authenticate.return_value = user # 2
        response = self.client.post('/accounts/login', {'assertion':'a'}) # 3
        self.assertEqual(response.content.decode(), 'OK') # 4
        
    

    @patch('accounts.views.authenticate')
    def test_gets_logged_in_session_if_authenticate_returns_a_user(
        self, mock_authenticate
    ):
        '''
        1: Mocked object should create a session if authenticate view function
        returns user, here we test that a session key was generated
        '''
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))  #1


    
    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(
        self, mock_authenticate
    ):
        '''
        1: validate that a session key was not created when mock_authenticate.return_value
        is set to None, or in otherwords login failed
        '''
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertNotIn(SESSION_KEY, self.client.session)  #1
        
    
    
    @patch('accounts.views.login') # 1
    @patch('accounts.views.authenticate') # 1a
    def test_calls_auth_login_if_authenticate_returns_a_user(
        self, mock_authenticate, mock_login # 1b
    ):
        '''
        1, 1a, 1b: notice order of nested patch decs and order of parameters
        2: Create request object with specific .POST data
        3: create mock_user as return object of mock_authenticate function
        4: Call relevant view function with relevant request
        5: Validate that when view function is called, authenticate function is called
        '''
        request = HttpRequest()
        request.POST['assertion'] = 'asserted' # 2
        mock_user = mock_authenticate.return_value # 3
        persona_login(request) # 4
        mock_login.assert_called_once_with(request, mock_user) # 5
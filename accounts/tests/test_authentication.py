
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)


@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

     
    def setUp(self):
        '''
        Notice we mock up requests.post so we don't send actual request
        '''
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        user.username = 'otheruser'  
        user.save()

        
        
    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        '''

        1: Create instance of our backend, call authenticate function on string
        2: Verify that there was response.post object sent with string under key "assertion"
        and domain under key "audience". This is testing the request sent more than the function
        '''
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': DOMAIN}
        )
        

    def test_returns_none_if_response_errors(self, mock_post):
        '''
        1: Modify mock return_value to false and the json.return value to what it would be
        2: Authenticate user with this data
        3: Verify that the 
        '''
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {} # 1
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)


    def test_returns_none_if_status_not_okay(self, mock_post):
        '''
        1: We change a value in the json this time instead
        '''
        mock_post.return_value.json.return_value = {'status': 'not okay!'}  #1
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)
        
    def test_finds_existing_user_with_email(self, mock_post):
        '''
        1: Create mock post object as if persona returned verified user
        2: Use ORM API to create User object using email provided in mock_post
        3: Run auth backend function with string as input
        4: Validate that our auth funciton takes the object we created previously
        and authenticates him, ei that request.post[data] and backend authentication are bound
        '''
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        actual_user = User.objects.create(email='a@b.com')
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(found_user, actual_user)
        
    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        '''
        1: Persona response object with stats: ok and user json object for valid assertion
        2: Run authenticate on persona object
        3: Retrive user by email, assuming User.objects.create() was run
        4: Validate that create() was run with proper user data
        '''
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@b.com')
        self.assertEqual(found_user, new_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        '''
        1: Create dummy user 
        2: Create new user by email
        3: Retrieve new user by email by passing his email to get_user()
        4: Test that created new user and retrieved new user are same
        '''
        backend = PersonaAuthenticationBackend()
        other_user = User(email='other@user.com')
        other_user.username = 'otheruser'
        other_user.save() # 1
        desired_user = User.objects.create(email='a@b.com') # 2
        found_user = backend.get_user('a@b.com') # 3
        self.assertEqual(found_user, desired_user) # 4


    def test_returns_none_if_no_user_with_that_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(
            backend.get_user('a@b.com')
        )



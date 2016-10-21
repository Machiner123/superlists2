from selenium.webdriver.common.action_chains import ActionChains
from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep



class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        edith_email = 'edith@example.com'
        edith_user_url= '/' + 'lists' + '/' + 'users' + '/' + edith_email + '/'
        self.create_pre_authenticated_session(edith_email)

        # She goes to the home page and starts a list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Reticulate splines\n')
        self.get_item_input_box().send_keys('Immanentize eschaton\n')
        first_list_url = self.browser.current_url
        #first_url_parts = first_list_url.split('/')
        #first_href_value = '/' + first_url_parts.split(-3) + '/' + 
        #    first_url_parts.split(-2) + '/'

        # She notices a "My lists" link, for the first time.
        element1 = self.browser.find_element_by_xpath("//a[@href='" + edith_user_url + "']")

        action = ActionChains(self.browser)
    
        sleep(5)
        action.click(element1).perform()


        #self.browser.find_element_by_xpath("//a[@href='" + edith_user_url + "']").click()

        #self.browser.find_element_by_xpath("//a[contains(text(), 'My lists')]").click()

        # She sees that her list is in there, named according to its
        # first list item
        # She sees that her list is in there, named according to its
        # first list item
        #self.assertEqual(self.browser.find_element_by_xpath("//a[contains(text(), 'Reticulate splines')]/@href"),
        #        first_list_url)
        
        #self.browser.find_element_by_xpath("//a[@href='" + self.href_of_url(first_list_url) + "']").click()
        element2 = self.browser.find_element_by_partial_link_text('Reticulate splines')
        sleep(5)
        action.click(element2).perform()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )
        # She decides to start another list, just to see
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Click cows\n')
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element_by_xpath("//a[contains(text(), 'My lists')]").click()
        #self.browser.find_element_by_link_text('My lists').click()
        #self.browser.find_element_by_xpath("//a[contains(text(), 'Click cows')]").click()
        #self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out.  The "My lists" option disappears
        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        )
from selenium.webdriver.common.action_chains import ActionChains
from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
#from selenium import webdriver
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

        # She notices a "My lists" link, for the first time.
        element = self.browser.find_element_by_xpath("//a[@href='" + edith_user_url + "']")
        action = ActionChains(self.browser)
        sleep(5)
        action.click(element).perform()


        # she sees that her list is named according to its first line 
        element = self.browser.find_element_by_xpath("//a[contains(text(), 'Reticulate splines')]")
        action = ActionChains(self.browser)
        sleep(5)
        action.click(element).perform()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )
       

        # She decides to start another list, just to see
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Click cows\n')
        second_list_url = self.browser.current_url

        
        # She goes back to her lists page to see if the second one is there
        element = self.browser.find_element_by_xpath("//a[@href='" + edith_user_url + "']")
        action = ActionChains(self.browser)
        sleep(5)
        action.click(element).perform()
        
        # SHe clicks on it and checks the url of the new list
        element = self.browser.find_element_by_xpath("//a[contains(text(), 'Click cows')]")
        action = ActionChains(self.browser)
        sleep(5)
        action.click(element).perform()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out.  The "My lists" option disappears
        element = self.browser.find_element_by_xpath("//a[contains(text(), 'Log out')]")
        action = ActionChains(self.browser)
        sleep(5)
        action.click(element).perform()
        #self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        )
from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
import time

TEST_EMAIL = 'edith@mockmyid.com'


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        '''
        1: Pass 'Mozila Persona' to switch_to_window, where it will check
        2: authentication_email is persona's generated id
        3: We put in edieth's email
        4: id_logout is generated because she is logged in
        
        '''
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')  #1

        # Edith logs in with her email address
        ## Use mockmyid.com for test email
        self.browser.find_element_by_id(
            'authentication_email'  # 2
        ).send_keys('edith@mockmyid.com') #3
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Refreshing the page, she sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Terrified of this new feature, she reflexively clicks "logout"
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)

        # The "logged out" status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(email=TEST_EMAIL)


    def switch_to_new_window(self, text_in_title):
        '''
        1: selenium stores multiple windows in window_handles, iterate through them
        2: pass each to selenium's own function to switch to a particular window
        3: check window for title we passed to this function from test_login, return
        '''
        retries = 20
        while retries > 0:
            for handle in self.browser.window_handles: # 1
                self.browser.switch_to_window(handle) # 2
                if text_in_title in self.browser.title: # 3
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')
        
    
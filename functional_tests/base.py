from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from unittest import skip


class FunctionalTest(StaticLiveServerTestCase):  

    @classmethod
    def setUpClass(cls): 
        '''
        This whole class method tries to circumvent our initial setUp() that uses the test server
        to use a real server. If we want a real erver, we put it in a command line argument.
        sys.argv is list of command line arguments passed to the script.
        We look for 'liveserver = url', split it into arg = [['liveserver'], ['url']],
        then store 'http://' + 'arg[1]' in cls.server_url
        ''' #1
        for arg in sys.argv:  #2
            if 'liveserver' in arg:  #arg will contain 'liveserver' = 'url'
                #split it into a list=['liveserver', 'url'], with list[1] = 'url'
                cls.server_url = 'http://' + arg.split('=')[1]  #4
                return  # this makes it an if-else
        super().setUpClass()  # this does not call the method within the method, this makes
                              # the method callable by other subclasses
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):  
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])



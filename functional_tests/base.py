from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from unittest import skip


class FunctionalTest(StaticLiveServerTestCase):  

    @classmethod
    def setUpClass(cls): 
        '''
        unittest has its own practice server, but we want to use a live server, so we
        write command line argument "liveserver = url". If there is such a command,
        we change server_url method of StaticLiveServerTestCase to 'http://' + 'url'.
        If there is no command line liveserver=url, we refer to the next definition
        of setUpClass in the method search tree using super, and use the class's
        default server test. live_server_url is set by --liveserver
        ''' #1
        for arg in sys.argv:  #2
            if 'liveserver' in arg:  #arg will contain 'liveserver' = 'url'
                #split it into a list=['liveserver', 'url'], with list[1] = 'url'
                cls.server_url = 'http://' + arg.split('=')[1]  #4
                return  
        super().setUpClass()  
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



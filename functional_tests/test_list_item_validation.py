from .base import FunctionalTest
from unittest import skip



class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url) ## get value of key server_id in dict
        self.get_item_input_box().send_keys('\n') ## element is sent empty white space

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        ## this is the page rendered with {"error":error} when there is a validation error
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        ## list_.delete() in views is why Get milk is #1
        self.get_item_input_box().send_keys('Get milk \n')
        self.check_for_row_in_list_table('1: Get milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Get milk') ## no browser because check is in db
        error=self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Get milk') 
        self.check_for_row_in_list_table('2: Make tea') 


    def test_cannot_add_duplicate_items(self):
         # Edith goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from lists.views import home_page
from django.utils.html import escape


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        '''
        instantiate resolve object, check it's .func attribute for the right
        view 
        '''
        found = resolve('/')  
        self.assertEqual(found.func, home_page)  
    
    def test_home_page_returns_correct_html(self):
        '''
        instantiate HttpRequest object, pass it through home_page view, check
        response for correctly rendered home.html. Notice render_to_string and .decode()
        both compile data to string format for comparison
        '''
        request = HttpRequest()  
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        

                

class ListViewTest(TestCase):
        
    def test_uses_list_template(self):
        '''
        create list object, which will have automatically generated list.id. Pass url
        to client get request, which comes up with what a browser would see. Check this rendered 
        template used our list.html template
        '''
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        '''
        since items are assigned a list, we run create obect on two different lists, 
        pass one list to client, check that the response contains items from
        the right list instead of another
        '''
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
    
    def test_passes_correct_list_to_template(self):
        '''
        notice first what is passed to assertEqual: context attribute of response, and 
        the list that was created and later used to create get request. this does not test
        template's rendering of the list, but simply the response's context
        '''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
        



class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        '''
        send a post request with specific context dict and count how many new 
        objects were created, then check that the data entered is the same
        as the data stored in item
        '''
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')



    def test_redirects_after_POST(self):
        '''
        client sends post request to lists/new, makes sure the view associated
        redirects to lists/list.id
        '''
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """
        pass post request with empty value for item_text, make sure the right
        template is used, the right status code is returned, make sure
        user is given error describing the mistake
        """
        response=self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item!")
        self.assertContains(response, expected_error) 
        
    def test_invalid_list_items_arent_saved(self):
        """
        make sure empty item data is not saved to objects or lists
        """
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)       


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''
        create two lists, send client post request to lists/%d/add_item
        with %d being the id of one of them, make sure the item data
        went to the right list
        '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        '''
        after adding data to list, make sure the view redirects to appropriate url
        '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))



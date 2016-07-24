from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        '''
        resolve checks if the url '/' leads anywhere, and it's func attribute
        is the view function that controls that url
        '''
        found = resolve('/')  
        self.assertEqual(found.func, home_page)  
    
    def test_home_page_returns_correct_html(self):
        '''
        we check if two different values are equal here, the veiws.home_page's output
        given an HttpRequest object as input, which is supposed to be home.html file. We
        then compare this to the home.html file passed through rendered_to_string.
        '''
        request = HttpRequest()  
        response = home_page(request)
        # think about similarities here between render and render to string:
        # render takes a temoplate and outs the html intp response.content,
        # while render_to_string takes html in a template and turns it into
        # a string so that the contents can be compared easily  
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        

        


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        '''
        store List() object in name list_, create two Item() objects with different .text
        but the same lis_ object stored in attribute .list, then check if data stored in DB
        actually matches what we want: two different .text values, and the same .list value
        '''
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
        
        
        

class ListViewTest(TestCase):
        
    def test_uses_list_template(self):
        '''
        create List instance as list_, which will have automatically generated unique .id
        attribute. Check that the template used under the url lists/list_.id matches our 
        list.html template
        '''
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        '''
        create two item objects with diff list values, the response from views
        if it has contains the right values and doesnt contain the wrong values
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
        two lists are created, but only one is passed as post request to views, and response
        is checked to see that it contains the one we passed and not the other
        '''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
        



class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        '''
        send a post request with specific context dict and 
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
        a post request is sent to url.py /lists/new, with 'A new list item'
        value stored in key 'item_text' in context dict(which new_list view
        stores as attribute .text of Item model). A list object is also created,
        and it's unique .id attribute is used to make a lists/.id string which is 
        supposed to be the url generated by our view. We check that the view works
        '''
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''
        two list objects are created in db without post request. Each having a unique
        .id, we can create two diff urls. A post request is sent to one of the urls,
        with specific .text data. We check that the list we created earlier and whos id we '
        used to make a url recieved that data.
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
        test the output of views.add_new_item, which is a redicrect to lists/list_.id
        '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))



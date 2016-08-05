from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError




    
def home_page(request):
    '''
    If request mthod = POST, create item in db with text from the 
    value of key "item_text" in POST QuertDict. If method is not post,
    simply render the 'home.html' template with the request info
    '''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


    
def new_list(request):
    '''
    When someone clicks on {{block form-action}}:
    Create list, item object with data from post request. Turn off dango's
    validation, try to save the item. If there is a validation error, delete
    the saved instance and display appropriate error. Render home, pass dict with
    "error":error to pass the error to the template. If exception not raised,
    meaning itm is non empty, redirecti to lists/list.id, which url conf reads as
    lists/(\d)/
    '''
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list = list_)
    try:    
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error="You can't have an empty list item!"
        return render(request, 'home.html', {"error":error})
    return redirect('/lists/%d/' % (list_.id))
    
    
def view_list(request, list_id):
    '''
    When the urlconf matches input url to lists/(/d+), the /d+ is stored in var
    list_id, and we create an run object.get on an instance of list, with id=list_id,
    and the name of the instace as list_. We return a rendered home page, with list_
    passed as value under the 'list' key in a dict
    '''
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def add_item(request, list_id):
    '''
    When list.html is rendered, and form_action link is clicked, the url lists/\d+/
    add_item maps to this, which takes captured list_id, runs object.get with
    captured data, and stores it in list_. We run item.objects.create with 
    request.POST['item_text'] data, and associate it to list_. We redirect
    to lists/\d/ url, which calls views.view_list
    '''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
    

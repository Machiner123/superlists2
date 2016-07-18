from django.shortcuts import redirect, render
from lists.models import Item, List



    
def home_page(request):
    '''
    if post is recieved, redirect to list_id url. other wise render static home.html
    '''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')

def view_list(request, list_id):
    '''
    get all the list objects from request matching list_id, filter items objects that
    have the common list object. Pass these items to list.html and render it
    '''
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

    
def new_list(request):
    '''
    store created list objects in list_, create item objects with values stored in context
    under key['item_text'] and list_ object stored in list. take the .id attribute of list_
    and make it the url of the new items objects filtered by list
    '''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = list_)
    return redirect('/lists/%d/' % (list_.id))


def add_item(request, list_id):
    '''
    get list objects from DB by the id that was passed along with POST request and store in list_, 
    create Item objects with text attrtibute stored in key item_text in context dict, 
    with data stored in list attribute coming fron list_. Redirect user to url /lists/list_.id
    '''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
    

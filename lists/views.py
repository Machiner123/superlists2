from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError




    
def home_page(request):
    '''
    reverses to "/", checks the request method, if POST uses db api command
    and kwarg stored in POST form data QueryDict, redirects to our only list
    as of now, or else returns home, rendered with request data
    '''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


    
def new_list(request):
    '''
    reverses to /lists/new/ url, creates instances of object creation from POST
    data. full_clean() turns of django's automatic list validation, then item is 
    saved. If validation fails on save, we render home with a msg to the user
    not to save empty lists. otherwise redirect to a url with the list_ id
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
    reverses to /list/list_.id/ url. instantiate object list get with list.id
    passed to it from url,
    render list.html with context from list object
    '''
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def add_item(request, list_id):
    '''
    reverses to /lists/add_item/, instantiates list object git on list id
    passed through urlconf, instantiates item object create with post form data,
    redirects to lists/list_.id, which calls view_list
    '''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
    

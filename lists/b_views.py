from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError




    
def home_page(request):
    
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
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error":error})
    return redirect(list_)
    
    
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    
    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
        
    return render(request, 'list.html', {'list': list_, 'error': error})



    

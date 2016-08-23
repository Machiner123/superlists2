from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    '''
    Pass POST dict to ItemForm constructor; only talk to model if data is valid;
    if valid create lis instance and object with data stored in POST dict under 
    key 'text', redirect to url named view_list in lists.urls, stored in get_absolute_url
    attr in list_.; else render home again, pass it the form  
    '''
    form = ItemForm(data = request.POST)
    if form.is_valid():
        list_=List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
    


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})
    
    
    

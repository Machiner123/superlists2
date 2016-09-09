from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})



def new_list(request):
    '''
    URLconf calls this function when data is inputed to form on home page.
    Instantiate and save ItemForm object, with data taken from request.POST.
    If is_valid returns True, use ItemForm's modified save(), return to 
    list_'s get_absolute_url attribute (calls view_list). If is_valid() returns
    False, return to homepage and pass the homepage template our form object
    '''
    form = ItemForm(data = request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
    


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})
    
    
    

from django.shortcuts import render
from .models import Apertment , Image
from django.core.paginator import Paginator

def products(request):
    image = Image.objects.all()
    product = Apertment.objects.all()[:5000]
    mylist = {}
    for pro in product:
        mylist[pro] = image.filter(Apertment_Id=pro.Apertment_Id).first()

    # Apply paginator
    paginator = Paginator(list(mylist.items()), per_page=12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Properties.html', {'page_obj': page_obj})
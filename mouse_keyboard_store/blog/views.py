from django.shortcuts import render
from .models import Blog
from shop.models import Slider


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def all_blog(request):
    # get slider
    slider = Slider.objects.filter(position = '4').latest('datecreate')
 
    context = {
        'Slider' : slider,
    }

    return render(request, 'blog/index.html', context)
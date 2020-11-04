from django.shortcuts import render
from .models import Blog


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def all_blog(request):
 
    context = {
        # 'Random_Products' : random_products,
    }

    return render(request, 'blog/index.html', context)
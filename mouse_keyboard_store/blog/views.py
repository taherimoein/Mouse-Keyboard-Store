from django.shortcuts import render
from .models import Blog
from shop.models import Slider
from django.core.paginator import Paginator


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def all_blog(request):
    # get slider
    slider = Slider.objects.filter(position = '4').latest('datecreate')
    # get blog post
    post_list = Blog.objects.filter(publish = True).order_by('-datecreate')
    # post paginator
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
 
    context = {
        'Slider' : slider,
        'PostList' : posts,
    }

    return render(request, 'blog/index.html', context)
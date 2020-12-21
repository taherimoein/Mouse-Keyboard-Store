from django.shortcuts import render
from .models import Blog
from shop.models import Slider
from django.core.paginator import Paginator
from django.db.models import Q


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def all_blog(request, words = None):
    if request.method != 'POST':
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
    else:
        words = request.POST["search"]
        # search word
        words = words.split(' ')
        words = list(filter(lambda i: i!='', words))
        search_words = []
        for word in words:
            search_word = list(map(lambda x: x + '\s*', word.replace(' ','')[:-1]))
            search_word = ''.join(search_word) + word[-1]
            search_words.append(search_word)
        search_word = r'.*'.join(search_words)
        # get slider
        slider = Slider.objects.filter(position = '4').latest('datecreate')
        # get blog post
        post_list = Blog.objects.filter(publish = True, title__regex = search_word).order_by('-datecreate')
        # post paginator
        paginator = Paginator(post_list, 2)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    
        context = {
            'Slider' : slider,
            'PostList' : posts,
        }

        return render(request, 'blog/index.html', context)

def single_blog(request, slug):
    # get blog post
    this_post = Blog.objects.get(slug = slug)
 
    context = {
        'This_post' : this_post,
    }

    return render(request, 'blog/blog-details.html', context)
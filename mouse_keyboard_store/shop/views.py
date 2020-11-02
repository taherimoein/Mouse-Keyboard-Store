from django.shortcuts import render

# Create your views here.

def index(request):
    # if request.user.is_authenticated:
 

    # context = {
        
    # }

    return render(request, 'shop/index.html')


# def a(request):

#     return render(request, 'shop/index.html')
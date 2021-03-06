from django.shortcuts import render, redirect
from shop.models import Product, Slider, Factor, FactorPost
from blog.models import Blog
import json, random


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# get random product list
def get_random_product_list():
    product_list = list(Product.objects.filter(publish = True))
    result = []
    count = len(product_list)

    while (count != 0) and (len(result) != 6):
        random_item = random.randint(0, (count - 1))
        result.append(product_list[random_item])
        product_list.remove(product_list[random_item])
        count -= 1

    return result

# get random disproduct list
def get_random_disproduct_list():
    product_list = list(Product.objects.filter(discount__gt = 0, publish = True))
    result = []
    count = len(product_list)

    while (count != 0) and (len(result) != 8):
        random_item = random.randint(0, (count - 1))
        result.append(product_list[random_item])
        product_list.remove(product_list[random_item])
        count -= 1

    return result

def index(request):
    # get random products
    random_products = get_random_product_list()
    # get top products
    top_products = get_random_disproduct_list()
    # get sliders
    sliders = Slider.objects.filter(position = 0, publish = True)
    # get ads banner
    ads_banner = Slider.objects.filter(position = 1, publish = True)
    # get blog post
    blog_posts = Blog.objects.filter(publish = True).order_by('-datecreate')[:3]
 
    context = {
        'Random_Products' : random_products,
        'Top_Products' : top_products,
        'AdsBanner' : ads_banner,
        'BlogList' : blog_posts,
        'Sliders' : sliders,
    }

    return render(request, 'shop/index.html', context)


def singel_product(request, id):
    # get this product
    this_product = Product.objects.get(id = id)
    # get top products
    top_products = get_random_disproduct_list()
 
    context = {
        'ThisProduct': this_product,
        'Images':this_product.image_list[:5],
        'Top_Products' : top_products,
    }

    return render(request, 'shop/product-details.html', context)


def about_us(request):
    # get sliders
    top_slider = Slider.objects.get(position = 2, publish = True)

    context = {
        'Slider' : top_slider,
    }

    return render(request, 'shop/about.html', context)


def show_cart(request):
    if request.user.is_authenticated:
        if Factor.objects.filter(FK_User = request.user, PaymentStatus = False).exists():
            # get user last factor
            this_factor = Factor.objects.get(FK_User = request.user, PaymentStatus = False)
            for item in this_factor.FK_FactorPost.all():
                if item.Endprice == 0:
                    item.end_price()

            context = {
                'ThisFactor' : this_factor,
            }

            return render(request, 'shop/card.html', context)
        else:
            return redirect("shop:index_page")
    else:
        return redirect("shop:sign_in_page")





def contact_us(request):
    # get sliders
    # top_slider = Slider.objects.get(position = 2, publish = True)

    context = {
        # 'Slider' : top_slider,
    }

    return render(request, 'shop/contact.html', context)


def sign_in(request):

    return render(request, 'registration/signin.html')


def sign_up(request):

    return render(request, 'registration/signup.html')


# # add products to db
# def add_products_to_db(request):

#     # read json file
#     with open("mouse_keyboard_store/data_keyboards.json", encoding = 'utf8') as data:
#         this_file = json.load(data)
#     # add data to db
#     print(str(len(this_file)))
#     for item in this_file:
#         this_title = item['title']
#         this_description = item['description']
#         this_image_list = item['ImagesUrl']
#         this_top_image = this_image_list[0]
#         this_image_list.remove(this_top_image)
#         this_point = float(item['point'])
#         this_price = ''.join(item['price'].split(','))
#         this_attributes = item['Params']
#         # this product
#         this_product = Product.objects.create(title = this_title, description = this_description, point = this_point, price = this_price, top_image = this_top_image, publish = True)
#         # set image list
#         this_product.image_list = this_image_list
#         this_product.save()
#         # set attributes
#         this_product.save_attributes(this_attributes)
#         print(str(len(this_file) - 1))

#     return render(request, 'shop/about.html')
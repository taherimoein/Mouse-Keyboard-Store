from rest_framework.decorators import api_view, permission_classes
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
# from .serializers import *
from kavenegar import *
import threading, random, string, datetime

# get model
from shop.models import OptionMeta, Contactus, Factor, FactorPost, Product
from blog.models import Blog

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# add to newsletters //req : get email form request //result: ({'status' : (True, False), 'message' : msg}) OR error
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def add_to_newsletters(request):
    try:
        # get data
        this_email = request.POST.get("email")
        # check newsletters list
        if OptionMeta.objects.filter(title = 'newsletters').exists():
            newsletters_list = OptionMeta.objects.get(title = 'newsletters')
        else:
            newsletters_list = OptionMeta.objects.create(title = 'newsletters', content = {'email_list' : []})
        # check email status
        if this_email in newsletters_list.content['email_list']:
            return JsonResponse({'status' : True, 'message' : '200'} , status = HTTP_200_OK)
        else:
            # add new email
            newsletters_list.content['email_list'].append(this_email)
            newsletters_list.save()
            # send new email
            subject, from_email, to = 'عضویت در خبرنامه سایت keymou', 'info@keymou.ir', this_email
            text_content = 'عضویت شما در خبرنامه keymou تبریک می گوییم!'
            html_content = '<h1 style="text-align: center;"><img src="https://s16.picofile.com/file/8413396668/logo_menu_navbar.pngy" alt="logo" width="161" height="69" /></h1> <h2 style="text-align: right;"><span style="color: #333399;">شما با موفقیت در خبرنامه سایت ما&nbsp;</span><span style="color: #333399;"><span style="color: #333399;">عضو شدید، از این بابت بسیار خرسندیم.</span></span></h2> <h3 style="text-align: right;"><span style="color: #000000;">با عضویت در این خبرنامه می توانید از&nbsp;</span></h3> <ul style="text-align: right;"> <li style="padding-left: 30px;"><span style="color: #000080;">جدید ترین محصولات</span></li> <li style="padding-left: 30px;"><span style="color: #000080;">جدید ترین مطالب وبلاگ</span></li> <li style="padding-left: 30px;"><span style="color: #000080;">جدید ترین تخفیفات سایت</span></li> </ul> <p style="text-align: right;"><span style="color: #000000;">در سریع ترین زمان با خبر شود.</span></p> <p style="text-align: left;"><a title="آدرس سایت ما" href="https://keymou.ir/" target="_blank" rel="noopener">keymou.ir</a></p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse({'status' : True, 'message' : '201'} , status = HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'status' : False, 'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


# set session
def set_session(request):
    response_data = {}
    try:
        this_path = request.POST['this_path']
        # get path other than non-account path 
        if not ((this_path == '/signin/') or (this_path == '/signup/') or (this_path == '/forgotpassword/')):
            request.session['next'] = this_path
        response_data['status'] = True
        return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# add connect us
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def add_new_connectus(request):
    try:
        # get data
        this_name = request.POST.get("this_fullname")
        this_mobile = request.POST.get("this_mobile")
        this_email = request.POST.get("this_email")
        this_message = request.POST.get("this_message")
        # check data
        if (len(this_name) > 0) and ((len(this_mobile) > 0) or (len(this_email) > 0)) and (len(this_message) > 0):
            # create new connect us
            this_connectus = Contactus.objects.create(full_name = this_name, description = this_message)
            # check mobile
            if this_mobile != 'null':
                this_connectus.mobile = this_mobile
            # check email
            if this_email != 'null':
                this_connectus.email = this_email
            # save data
            this_connectus.save()

            return JsonResponse({'status' : True}, status = HTTP_201_CREATED)
        else:
            return JsonResponse({'status' : False, 'message' : 'Input data is incomplete'}, status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status' : False, 'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


# add comment
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def add_new_comment(request):
    try:
        # get data
        this_post_id = request.POST.get("this_post")
        this_name = request.POST.get("this_fullname")
        this_message = request.POST.get("this_message")
        # check data
        if (len(this_name) > 0) and (len(this_message) > 0):
            # get this post
            this_post = Blog.objects.get(id = this_post_id)
            # add comment
            this_post.save_comment(this_name, this_message)

            return JsonResponse({'status' : True}, status = HTTP_201_CREATED)
        else:
            return JsonResponse({'status' : False, 'message' : 'Input data is incomplete'}, status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status' : False, 'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


# add to card
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_card(request):
    try:
        # get data
        this_product_id = request.POST.get("this_product")
        this_count = request.POST.get("this_count")
        # check data
        if len(this_count) > 0:
            # check factor
            if Factor.objects.filter(PaymentStatus = False, FK_User = request.user).exists():
                this_factor = Factor.objects.get(FK_User = request.user, PaymentStatus = False)
                # get this product
                this_product = Product.objects.get(id = this_product_id)
                if this_factor.FK_FactorPost.filter(FK_Product = this_product).exists():
                    this_item = this_factor.FK_FactorPost.get(FK_Product = this_product)
                    this_item.ProductCount += int(this_count)
                else:
                    this_item = FactorPost.objects.create(FK_Product = this_product, ProductCount = int(this_count))
                    Factor.objects.filter(PaymentStatus = False, FK_User = request.user)[0].FK_FactorPost.add(this_item)
            else:
                this_factor = Factor.objects.create(FK_User = request.user, PaymentStatus = False)
                this_product = Product.objects.get(id = this_product_id)
                this_item = FactorPost.objects.create(FK_Product = this_product, ProductCount = int(this_count))
                this_factor.FK_FactorPost.add(this_item)

            return JsonResponse({'status' : True}, status = HTTP_200_OK)
        else:
            return JsonResponse({'status' : False, 'message' : 'Input data is incomplete'}, status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status' : False, 'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


# update_factor
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_factor(request):
    try:
        # get data
        this_phone = request.POST.get("this_phone")
        this_address = request.POST.get("this_address")
        this_zip = request.POST.get("this_zip")
        this_state = request.POST.get("this_state")
        this_city = request.POST.get("this_city")
        this_bigcity = request.POST.get("this_bigcity")
        # check data
        if (len(this_phone) > 0) and (len(this_address) > 0) and (len(this_zip) > 0) and (len(this_state) > 0) and (len(this_city) > 0) and (len(this_bigcity) > 0):
            # get this factor
            this_factor = Factor.objects.get(FK_User = request.user, PaymentStatus = False)
            this_factor.MobileNumber = this_phone
            this_factor.ZipCode = this_zip
            this_factor.Address = this_address
            this_factor.City = this_city
            this_factor.BigCity = this_bigcity
            this_factor.State = this_state
            total_price = 0
            for item in this_factor.FK_FactorPost.all():
                total_price += item.Endprice
            this_factor.TotalPrice = total_price
            this_factor.PaymentStatus = True
            this_factor.save()
   
            return JsonResponse({'status' : True}, status = HTTP_200_OK)
        else:
            return JsonResponse({'status' : False, 'message' : 'Input data is incomplete'}, status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status' : False, 'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)
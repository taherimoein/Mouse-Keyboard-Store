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
from shop.models import OptionMeta

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
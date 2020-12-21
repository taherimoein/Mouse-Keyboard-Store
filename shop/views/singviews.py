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
from django.shortcuts import render
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
from shop.models import User, Validation

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# check mobilenumber //req : get mobile number form request //result: ({'status' : (True, False), 'message' : (200, 404, msg)}) OR error
def check_mobilenubmer(request):
    response_data = {} 
    try: 
        mobile = request.POST.get("mobile")
        if User.objects.filter(mobile = mobile).exists():
            response_data['status'] = True
            response_data['message'] = '200'
            return JsonResponse(response_data)
        else:
            response_data['status'] = True
            response_data['message'] = '404'
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# send sms
def send_sms(mobilenumber, text):
    try:
        api = KavenegarAPI('2B485230622F74625978584E343167657576785041736B4A586D6E524C4661577A56566B44366D674C75413D')
        params = {
            'receptor': mobilenumber,
            'message': text,
        } 
        response = api.sms_send(params)
        print(response)
    except Exception as e: 
        print(e)


# account singup //req : get user info form request //result: ({'status' : (True, False), 'message' : msg}) OR error
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def singup(request):
    try:
        # get data
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        mobilenumber = request.POST.get("mobile")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        # check password and repeat password
        if password == repeat_password:
            # create new user
            this_user = User.objects.create_user(mobilenumber, password = password)
            # set other data
            this_user.first_name = firstname
            this_user.last_name = lastname
            this_user.save()
            # send sms
            message = 'کاربر محترم ' + mobilenumber + ' شما با موفقیت در سایت keymou ثبت نام کردید.'
            send_sms(mobilenumber, message)
            # login user
            login(request, this_user)

            return JsonResponse({'status' : True, 'message' : '201'} , status = HTTP_201_CREATED)
        else:
            return JsonResponse({'status' : True, 'message' : '400'} , status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status' : False, 'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)



# account singin //req : get mobilenumber and password form request //result: ({'status' : (True, False), 'message' : (200, 400, msg)}) OR error
def singin(request):
    response_data = {}
    try:
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        # set status
        if remember_me == '1':
            status = True
        else:
            status = False
        # check user
        user = authenticate(request, mobile = mobile, password = password)
        # get next page
        next_page = settings.LOGIN_URL
        if 'next' in request.session:
            next_page = request.session['next']
        if user is not None:
            # login user
            login(request, user)
            if status:
                session_key = request.session.session_key or Session.objects.get_new_session_key()
                Session.objects.save(session_key, request.session._session, timezone.now() + datetime.timedelta(seconds = settings.SESSION_COOKIE_AGE))
            response_data['status'] = True
            response_data['message'] = '200'
            response_data['next'] = next_page
            return JsonResponse(response_data)
        else:
            response_data['status'] = True
            response_data['message'] = '400'
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)



# account signout //req : request //result: ({'status' : (True, False)}) OR error
def signout(request):
    if request.user.is_authenticated: 
        logout(request)
        return redirect("shop:index_page")
    else:
        return redirect("shop:index_page")



# account change password //req : get password form request //result: ({'status' : (True, False), 'message' : (200, msg)}) OR error
def change_password(request):
    response_data = {}
    try:
        new_password = request.POST.get("new_password")
        repeat_password = request.POST.get("repeat_password")
        # check password and repeat password
        if new_password == repeat_password:
            # get user
            this_user = request.user
            # change password
            this_user.set_password(new_password)
            # sing out user
            logout(request)

            response_data['status'] = True
            response_data['message'] = '200'
            return JsonResponse(response_data)
        else:
            response_data['status'] = True
            response_data['message'] = '400'
            return JsonResponse(response_data)

    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)



# account forget password //req : get mobile number and password form request //result: ({'status' : (True, False), 'message' : (200, msg)}) OR error
def forget_password(request):
    response_data = {}
    try:
        mobile = request.POST.get("mobile")
        new_password = request.POST.get("new_password")
        repeat_password = request.POST.get("repeat_password")
        # check password and repeat password
        if new_password == repeat_password:
            # get user
            this_user = User.objects.get(mobile = mobile)
            # change password
            this_user.set_password(new_password)

            response_data['status'] = True
            response_data['message'] = '200'
            return JsonResponse(response_data)
        else:
            response_data['status'] = True
            response_data['message'] = '400'
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# send verify code with kavengar api
class send_verify_code(threading.Thread):
    def run(self, mobile, verify_code):
        try:
            api = KavenegarAPI('2B485230622F74625978584E343167657576785041736B4A586D6E524C4661577A56566B44366D674C75413D')
            params = {
                'receptor': mobile,
                'template': 'verify-code',
                'token': verify_code,
                'type': 'sms',
            }   
            api.verify_lookup(params)

            return True
        except Exception as e:
            print('send-verify-code-log : ' + str(e))
            return False


# create verify code when sgin up
def create_verify_code(request):
    response_data = {}
    try:
        # get data
        mobile = request.POST.get("mobile")
        # check user
        if not User.objects.filter(mobile = mobile).exists():
            # create verify code
            verify_code = ''.join(random.choice(string.digits) for i in range(6))
            # add to validation tb
            Validation.objects.create(mobile = mobile, valid_code = verify_code)
            # send verify code for user
            result = send_verify_code().run(mobile, verify_code)
            if result:
                response_data['status'] = True
                response_data['message'] = '200'
                return JsonResponse(response_data)
            else:
                response_data['status'] = True
                response_data['message'] = '400'
                return JsonResponse(response_data)
        else:
            response_data['status'] = True
            response_data['message'] = '404'
            return JsonResponse(response_data)
    except Exception as e: 
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# create verify code when forget password
def forget_password_verify_code(request):
    response_data = {}
    try:
        # get data
        mobile = request.POST.get("mobile")
        # check user
        if User.objects.filter(mobile = mobile).exists():
            # create verify code
            verify_code = ''.join(random.choice(string.digits) for i in range(6))
            # get validation record
            if Validation.objects.filter(mobile = mobile).exists():
                this_verify_code = Validation.objects.get(mobile = mobile)
                # add new code
                this_verify_code.valid_code = verify_code
                this_verify_code.save()
            # send verify code for user
            result = send_verify_code().run(mobile, verify_code)
            if result:
                response_data['status'] = True
                response_data['message'] = '200'
                return JsonResponse(response_data)
            else:
                response_data['status'] = True
                response_data['message'] = '400'
                return JsonResponse(response_data)
        else:
            response_data['status'] = True
            response_data['message'] = '404'
            return JsonResponse(response_data)
    except Exception as e: 
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)
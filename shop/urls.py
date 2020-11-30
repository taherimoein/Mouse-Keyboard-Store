from django.urls import path, re_path 
from .views import views, ajaxviews, singviews

app_name = 'shop'
urlpatterns = [
    # Index Path <----->
    path('', views.index, name = 'index_page'),
    # Session Path <----->
    path('set-session', ajaxviews.set_session, name = 'set_session'),
    # About us Path <----->
    path('about-us/', views.about_us, name = 'about_us_page'),
    # Contact us Path <----->
    path('contact-us/', views.contact_us, name = 'contact_us_page'),
    # Sing in Path <----->
    path('signin/', views.sign_in, name = 'sign_in_page'),
    # Sing up Path <----->
    path('signup/', views.sign_up, name = 'sign_up_page'),
    # Check Mobile Number <----->
    path('ajax/check/mobile-number/', singviews.check_mobilenubmer, name = 'ajax_check_mobilenumber'),
    # Sing in fun <----->
    path('ajax/singin/', singviews.singin, name = 'ajax_singin'),
    # Sing out fun <----->
    path('singout/', singviews.signout, name = 'singout'),

    # <====================================================================================>
    # Add To Newsletters Path <----->
    path('add/new-email/', ajaxviews.add_to_newsletters, name = 'add_to_newsletters'),
    # add new connect us api <----->
    path('add/connesct-us/', ajaxviews.add_new_connectus , name = 'create_new_connectus_api'),
]
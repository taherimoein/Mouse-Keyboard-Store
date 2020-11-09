from django.urls import path, re_path 
from . import views, ajaxviews

app_name = 'shop'
urlpatterns = [
    # Index Path <----->
    path('', views.index, name = 'index_page'),

    # Session Path <----->
    # path('set-session', views.set_session, name = 'set_session'),

    # About us Path <----->
    path('about-us/', views.about_us, name = 'about_us_page'),
    # Sing in Path <----->
    path('signin/', views.sign_in, name = 'sign_in_page'),
    # Sing up Path <----->
    path('signup/', views.sign_up, name = 'sign_up_page'),

    # <====================================================================================>
    # Add To Newsletters Path <----->
    path('add/new-email/', ajaxviews.add_to_newsletters, name = 'add_to_newsletters'),
]
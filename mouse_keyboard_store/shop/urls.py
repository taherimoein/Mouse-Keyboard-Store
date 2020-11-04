from django.urls import path, re_path 
from . import views

app_name = 'shop'
urlpatterns = [
    # Index Path <----->
    path('', views.index, name = 'index_page'),

    # Session Path <----->
    # path('set-session', views.set_session, name = 'set_session'),

    # About us Path <----->
    path('about-us/', views.about_us, name = 'about_us_page'),
]
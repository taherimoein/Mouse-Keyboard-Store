from django.urls import path, re_path 
from . import views

app_name = 'blog'
urlpatterns = [
    # All Blog Path <----->
    path('', views.all_blog, name = 'allblog_page'),
]
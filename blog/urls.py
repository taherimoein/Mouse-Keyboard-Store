from django.urls import path, re_path 
from . import views
from shop.views import ajaxviews

app_name = 'blog'
urlpatterns = [
    # All Blog Path <----->
    path('', views.all_blog, name = 'allblog_page'),
    # Single Blog Path <----->
    path('singel/<slug:slug>/', views.single_blog, name = 'single_blog_page'),
    # add comment
    path('ajax/add-comment/', ajaxviews.add_new_comment, name = 'add_new_comment'),
]
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, UserManager, Slider, OptionMeta, Product
from blog.models import Blog

User = get_user_model()
# Main Section Title
admin.site.site_header = 'Viscal'
# --------------------------------
# Blog Admin Section
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'summary', 'author', 'datecreate', 'publish')
    search_fields = ['title', 'slug', 'summary']
    list_filter = ('publish',)
    ordering = ['id', 'datecreate']
# Slider Admin Section
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'publish', 'datecreate')
    search_fields = ['title']
    list_filter = ('publish',)
    ordering = ['id', 'datecreate']
# OptionMeta Admin Section
@admin.register(OptionMeta)
class OptionMetaAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'content')
    search_fields = ['title']
    ordering = ['id']
# Product Admin Section
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'point', 'price', 'createdate', 'publish')
    search_fields = ['title', 'description']
    list_filter = ('publish',)
    ordering = ['id']
# User Admin Section
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mobile', 'email', 'createdate', 'active', 'superuser', 'staff')
    search_fields = ['mobile', 'first_name', 'last_name']
    list_filter = ('active','superuser','staff')
    ordering = ['id']
admin.site.register = (User, UserAdmin)
admin.site.register = (UserManager)
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from datetime import datetime
from django.http import JsonResponse
import random, json

# --------------------------------------------------------------------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def create_user(self, mobile, password = None, **kwargs):
        if not mobile:
            raise ValueError("Users must have mobile")
        if not password:
            raise ValueError("Users must have password")
        user = self.model(mobile = mobile, **kwargs)
        user.set_password(password)
        user.save()
        return user

    
    def create_staffuser(self, mobile, password, **kwargs):
        user = self.model(mobile = mobile, staff = True, **kwargs)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, mobile, password, **kwargs):
        user = self.model(mobile = mobile, staff = True, superuser = True, **kwargs)
        user.set_password(password)
        user.save()
        return user
        
# --------------------------------------------------------------------------------------------------------------------------------------

# User (کاربر) Model
class User (AbstractBaseUser):
    first_name = models.CharField(verbose_name = 'firstname', max_length = 150)
    last_name = models.CharField(verbose_name = 'lastname', max_length = 300)
    mobile = models.CharField(verbose_name = 'mobilenumber', max_length = 11, unique = True)
    email = models.EmailField(verbose_name = 'email', unique = True, blank = True, null = True)
    nationalcode = models.CharField(verbose_name = 'کد ملی', max_length = 10, blank = True, null = True)
    active = models.BooleanField(verbose_name = 'وضعیت فعالیت', default = True)
    superuser = models.BooleanField(verbose_name = 'وضعیت مدیریت', default = False)
    staff = models.BooleanField(verbose_name = 'وضعیت کارمندی', default = False)
    birthdate = models.DateField(verbose_name = 'تارخ تولد', blank = True, null = True)
    profile = models.ImageField(verbose_name = 'عکس پروفایل', upload_to = 'media/images/profile/', default = 'static/img/joblogo.png')
    SEX_TYPE =(
        (0,'انتخاب جنسیت'),
        (1,'زن'),
        (2,'مرد'),
        (3,'سایر'),
    )
    sex = models.PositiveSmallIntegerField(verbose_name = 'جنسیت', choices = SEX_TYPE, default = 0)
    address = JSONField(verbose_name = 'آدرس', null = True, blank = True)
    createdate = models.DateTimeField(verbose_name = 'تاریخ عضویت', auto_now_add = True)
    factors_list = ArrayField(models.BigIntegerField(), verbose_name = 'لیست فاکتور های کاربر', null = True, blank = True)
    saved_products_list = ArrayField(models.BigIntegerField(), verbose_name = 'محصولات ذخیره شده', null = True, blank = True)

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_staff(self):
        return self.staff

    def __str__(self):
       return "{} {}".format(self.first_name, self.last_name)

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_fullname(self):
        return self.first_name + ' ' + self.last_name

    def save_address(self, state = None, city = None, address = None, zipcode = None):
        if self.address is None:
            if state is not None:
                str_state =  str(state)
            else:
                str_state = None

            if city is not None:
                str_city =  str(city)
            else:
                str_city = None

            if address is not None:
                str_address =  str(address)
            else:
                str_address = None

            if zipcode is not None:
                str_zipcode =  str(zipcode)
            else:
                str_zipcode = None

            self.address = {'state' : str_state, 'city' : str_city, 'address' : str_address, 'zipcode' : str_zipcode}
            self.save()
        else:
            if state is not None:
                self.address['state'] =  str(state)

            if city is not None:
                self.address['city'] =  str(city)

            if address is not None:
                self.address['address'] =  str(address)

            if zipcode is not None:
                self.address['zipcode'] =  str(zipcode)
        
            self.save()

    class Meta:
        ordering = ('id',)   
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

#----------------------------------------------------------------------------------------------------------------------------------------

# Slider (اسلایدر) Model
class Slider(models.Model): 
    title = models.CharField(verbose_name = 'عنوان', unique = True, max_length = 255)
    POSITION_TYPE = (
        ('0','اسلایدر-صفحه اصلی'),
        ('1','بنر-وسط صفحه اصلی'),
        ('2','اسلایدر-صفحه درباره ما'),
        ('3','بنر-درباره ما'),
        ('4','اسلایدر- صفحه بلاگ'),
    )
    position = models.CharField(verbose_name = 'موقعیت مکانی', max_length = 1, choices = POSITION_TYPE, default = '0')
    image = models.ImageField(verbose_name = 'عکس', upload_to = 'media/images/slider/')
    datecreate = models.DateTimeField(verbose_name = 'تاریخ بارگذاری', auto_now_add = True)
    dtatupdate = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی', auto_now = True)
    PUBLISH_STATUS = (
        (True,'منتشر شده'),
        (False,'منتشر نشده'),
    )
    publish = models.BooleanField(verbose_name = 'وضعیت', choices = PUBLISH_STATUS, default = False)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id',)   
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"
    
#----------------------------------------------------------------------------------------------------------------------------------------

# OptionMeta (آپشن) Model
class OptionMeta(models.Model):
    title = models.CharField(verbose_name = 'عنوان', max_length = 255, unique = True)
    description = models.TextField(verbose_name = 'توضیحات', blank = True)
    content = JSONField(verbose_name = 'محتوا')

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ('id',)   
        verbose_name = "آپشن"
        verbose_name_plural = "آپشن ها"

# --------------------------------------------------------------------------------------------------------------------------------------

# Product (محصول) Model
class Product(models.Model):
    title = models.CharField(verbose_name = 'عنوان', unique = True, max_length = 255)
    description = models.TextField(verbose_name = 'توضیحات', blank = True)
    top_image = models.URLField(verbose_name = 'عکس شاخص', null = True, max_length = 255)
    image_list = ArrayField(models.URLField(max_length = 255), verbose_name = 'لیست عکس های محصول', null = True, blank = True)
    point = models.FloatField(verbose_name = 'امتیاز', default = 0.0)
    price = models.CharField(verbose_name = 'قیمت', max_length = 15)
    discount = models.PositiveSmallIntegerField(verbose_name = 'درصد تخفیف محصول', default = 0)
    inventory = models.PositiveSmallIntegerField(verbose_name = 'موجودی محصول', default = 20)
    attributes = JSONField(verbose_name = 'لیست ویژگی ها', null = True, blank = True)
    createdate = models.DateTimeField(verbose_name = 'تاریخ ثبت', auto_now_add = True)
    PUBLISH_STATUS = (
        (True,'منتشر شده'),
        (False,'عدم انتشار'),
    )
    publish = models.BooleanField(verbose_name = 'وضعیت انتشار', choices = PUBLISH_STATUS, default = False)

    def __str__(self):
        return "{}".format(self.title)

    def save_attributes(self, attribute_list):
        data = {}
        data['attributes'] = []
        # convert data
        for item in attribute_list:
            this_item = {
                "title": item,
                "value": attribute_list[item]
            }
            data['attributes'].append(this_item)

        self.attributes = data
        self.save()

    def get_url(self):
        return reverse("shop:single_product", kwargs = {
            'id': self.id,
        })

    class Meta:
        ordering = ('id',)   
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

#----------------------------------------------------------------------------------------------------------------------------------------

# Validation (اعتبار سنجی) Model   
class Validation(models.Model):
    mobile = models.CharField(verbose_name = 'شماره موبایل', max_length = 11, unique = True)
    valid_code = models.CharField(verbose_name = 'کد فعال سازی', max_length = 6, null = True)
    status = models.BooleanField(verbose_name = 'وضعیت', default = False)
    date = models.DateTimeField(verbose_name = 'تاریخ و زمان', auto_now_add = True)

    class Meta:
        ordering = ('id',)
    
# --------------------------------------------------------------------------------------------------------------------------------------

# Contact us (ارتباط با ما) Model
class Contactus(models.Model):
    full_name = models.CharField(verbose_name = 'نام و نام خانوادگی', max_length = 255)
    email = models.EmailField(verbose_name = 'ایمیل', null = True)
    mobile = models.CharField(verbose_name = 'موبایل', max_length = 11, null = True)
    description = models.TextField(verbose_name = 'توضیحات')
    createdate = models.DateTimeField(verbose_name = 'تاریخ', auto_now_add = True)
    SEEN_STATUS = (
        ('0','خوانده نشده'),
        ('1','در حال بررسی'),
        ('2','بررسی شده'),
    )
    status = models.CharField(verbose_name = 'وضعیت', max_length = 1, choices = SEEN_STATUS, default = '0')

    def __str__(self):
        return "{}".format(self.full_name)


    def get_status(self):
        status_type = {
            "0" : 'خوانده نشده',
            "1" : 'در حال بررسی',
            "2" : 'بررسی شده',
        }
        return status_type[self.status]
    
    class Meta:
        ordering = ('id',)
        verbose_name = "ارتباط با ما"
        verbose_name_plural = "ارتباط های با ما"



# FactorPost (محصولات فاکتور) Model
class FactorPost (models.Model):
    FK_Product=models.OneToOneField(Product, on_delete=models.SET_NULL, verbose_name='محصول', related_name='Factor_Product', null=True)
    ProductCount=models.PositiveIntegerField(verbose_name='تعداد محصول', default=1)
    Endprice = models.BigIntegerField(verbose_name='قیمت نهایی', default=0)

    def end_price(self):
        self.Endprice = int(self.FK_Product.price) * self.ProductCount
        self.save()

    def __str__(self):
        return "{}".format(self.FK_Product)
    
    # Ordering With DateCreate
    class Meta:
        ordering = ('id',)
        verbose_name = "محصول فاکتور"
        verbose_name_plural = "محصول فاکتور ها"
        
#----------------------------------------------------------------------------------------------------------------------------------

# Factor (فاکتور) Model 
class Factor(models.Model):
    FK_User = models.ForeignKey(User, on_delete = models.SET_NULL, verbose_name = 'صاحب فاکتور', related_name='UserFactor', null=True)
    MobileNumber=models.CharField(verbose_name='شماره موبایل', max_length=11, blank=True)
    ZipCode=models.CharField(verbose_name='کد پستی', max_length=10, blank=True)
    Address=models.CharField(verbose_name='آدرس', max_length=300, blank=True)
    City=models.CharField(verbose_name='شهر', max_length=50, blank=True)
    BigCity=models.CharField(verbose_name='شهرستان', max_length=50, blank=True)
    State =models.CharField(verbose_name='استان', max_length=50, blank=True)
    FK_FactorPost = models.ManyToManyField(FactorPost, verbose_name='محصولات فاکتور', related_name='Factor_Products', blank=True)
    TotalPrice=models.CharField(verbose_name='هزینه کل', max_length=15)
    PAYMENT_STATUS =(
        (True,'پرداخت شد'),
        (False,'پرداخت نشده'),
    )
    PaymentStatus=models.BooleanField(verbose_name='وضعیت پرداخت', choices=PAYMENT_STATUS, default=False)
    OrderDate=models.DateTimeField(verbose_name='تاریخ خرید', auto_now_add=True)
    ORDER_STATUS =(
        ('0','سفارش تحویل داده شده است'),
        ('1','سفارش آماده است'),
        ('2','سفارش در حال آماده سازی است'),
        ('3','منتظر بررسی'),
        ('4','سفارش لغو شده است'),
        ('5','سفارش ارسال شده است'),
    )
    OrderStatus=models.CharField(verbose_name='وضعیت سفارش', max_length=1, choices=ORDER_STATUS, default='3')

    # Output Customization Based On User, ID
    def __str__(self):
        return "{} ({})".format(self.FK_User, self.FactorNumber)

    # Ordering With DateCreate
    class Meta:
        ordering = ('id',)
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتور ها"

#----------------------------------------------------------------------------------------------------------------------------------
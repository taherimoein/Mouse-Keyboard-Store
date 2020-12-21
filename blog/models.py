from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from datetime import datetime
from django.shortcuts import reverse

# --------------------------------------------------------------------------------------------------------------------------------------

# Blog (بلاگ) Model
class Blog(models.Model): 
    title = models.CharField(verbose_name = 'عنوان', max_length = 255)
    slug = models.SlugField(verbose_name = 'شناسه')
    summary = models.CharField(verbose_name = 'خلاصه', max_length = 300)
    author = models.CharField(verbose_name = 'نویسنده', max_length = 450, null = True, blank = True)
    code = models.TextField(verbose_name = 'کد HTML')
    top_image = models.ImageField(verbose_name = 'عکس شاخص', upload_to = 'media/images/blog/')
    slider = models.ImageField(verbose_name = 'اسلایدر', upload_to = 'media/images/blog/slider/')
    reted_list = JSONField(verbose_name = 'لیست امتیاز', null = True, blank = True)
    liked_list = JSONField(verbose_name = 'لیست لایک', null = True, blank = True)
    datecreate = models.DateTimeField(verbose_name = 'تاریخ بارگذاری', auto_now_add = True)
    dtatupdate = models.DateTimeField(verbose_name = 'تاریخ بروزرسانی', auto_now = True)
    PUBLISH_STATUS = (
        (True,'منتشر شده'),
        (False,'منتشر نشده'),
    )
    publish = models.BooleanField(verbose_name = 'وضعیت', choices = PUBLISH_STATUS, default = False)

    def __str__(self):
        return "{}".format(self.title)

    def get_url(self):
        return reverse("blog:single_blog_page", kwargs = {
            'slug': self.slug,
        })

    def save_comment(self, name, message):
        if self.reted_list is not None:
            this_comment = {'name': name, 'message': message}
            this_list = list(self.reted_list['list'])
            this_list.append(this_comment)
            self.reted_list['list'] = this_list
            self.save()
        else:
            self.reted_list = {'list': []}
            this_comment = {'name': name, 'message': message}
            self.reted_list['list'] = this_comment
            self.save()


    class Meta:
        ordering = ('id',)   
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ ها"
    
#----------------------------------------------------------------------------------------------------------------------------------------
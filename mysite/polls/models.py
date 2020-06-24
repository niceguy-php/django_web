from django.db import models
import datetime
from django.utils import timezone
from multiselectfield import MultiSelectField
import os
from django.conf import settings
from django.utils.safestring import mark_safe
import uuid
# from django_thumbs.db.models import ImageWithThumbsField
# Create your models here.

def images_path():
    return settings.MEDIA_ROOT

def generate_filename(instance, filename):
    """
    安全考虑，生成随机文件名
    """
    directory_name = datetime.datetime.now().strftime('polls/%Y/%m/%d')
    filename = uuid.uuid4().hex + os.path.splitext(filename)[-1]
    return os.path.join(directory_name, filename)

class Question(models.Model):
    status_type = (('1', u'开启'), ('0', u'关闭'))
    language_choices = (('chinese', u'汉语'), ('english', u'英语'), ('french', '法语'))
    question_text = models.CharField(max_length=200)
    status = models.CharField(u"状态", choices=status_type,default="1",max_length=200)
    language = MultiSelectField(u"使用语言", choices=language_choices, null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    headImg = models.ImageField(upload_to=generate_filename, default="")
    is_disabled = models.BooleanField(u"是否启用",default=False)
    # coverImg = ImageWithThumbsField("封面",upload_to=generate_filename, sizes=((125, 125),))

    def __unicode__(self):
        return self.coverImg.url_150x150

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'



    def head_img_thumb(self):
        if self.headImg:
            img = mark_safe('<img src="/media/%s" width="50px" />' % (self.headImg,))
            return img
        else:
            return '(no image)'

    head_img_thumb.admin_order_field = 'headImg'
    head_img_thumb.short_description = u'头像'
    head_img_thumb.allow_tags = True
    readonly_fields = ['head_img_thumb']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
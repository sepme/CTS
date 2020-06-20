import os

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

#for Compress the news' photo
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import uuid

from ChamranTeamSite import settings


def upload_to(instance, file_name):
    return os.path.join(settings.MEDIA_ROOT, 'message_attachments', file_name)

def newsAttach(instance, file_name):
    return os.path.join(settings.MEDIA_ROOT, 'news', instance.title[:15], file_name)

def newsPicture(instance, file_name):
    return os.path.join(settings.MEDIA_ROOT, 'News Pictures', instance.news.title[:15], file_name)


class Message(models.Model):
    title = models.CharField(max_length=128, verbose_name="عنوان", default="بدون عنوان")
    text = models.TextField(verbose_name="متن پیام")
    date = models.DateField(auto_now_add=True, null=True)
    read_by = models.ManyToManyField(User, related_name='read_by', blank=True)
    code = models.CharField(max_length=15, verbose_name='کد', default='000-000')

    MESSAGE_TYPES = (
        (0, "اطلاعیه"),
        (1, "اخطار"),
        (2, "اخبار"),
    )

    type = models.IntegerField(default=0, choices=MESSAGE_TYPES, verbose_name="نوع")
    attachment = models.FileField(upload_to=upload_to, blank=True, null=True, verbose_name="ضمیمه")
    receiver = models.ManyToManyField(User, verbose_name="گیرندگان")

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > 30:
            return self.text[:30] + '...'
        return self.text

    @staticmethod
    def get_user_messages(user):
        user_messages = Message.objects.filter(receiver=user)
        return user_messages


class News(models.Model):
    title = models.CharField(max_length=128, verbose_name="عنوان", default="بدون عنوان")
    # text = models.TextField(verbose_name="متن خبر")
    text = RichTextUploadingField()
    attachment = models.FileField(upload_to=newsAttach, verbose_name="ضمیمه", blank=True, null=True)
    link = models.CharField(max_length=128, verbose_name="لینک خبر")
    writer = models.CharField(max_length=32, verbose_name="نویسنده")
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title[: 15]

    def get_absolute_url(self):
        return 'news/' + self.link

class Picture(models.Model):
    news = models.ForeignKey(News, verbose_name="خبر", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=newsPicture, verbose_name="تصویر خبر")

    def __str__(self):
        return str(self.news)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.picture = self.compressImage(self.picture)
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    def compressImage(self,photo):
        imageTemproary = Image.open(photo).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=40)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


class TempUser(models.Model):
    email = models.EmailField(max_length=254)
    unique = models.UUIDField(unique=True, default=uuid.uuid4)
    CHOICE = (
        ('expert', 'Expert'),
        ('industry', 'Industry'),
        ('researcher', 'Researcher')
    )
    account_type = models.CharField(max_length=50, choices=CHOICE)

    def __str__(self):
        return self.account_type + ' - ' + str(self.email)

    def get_absolute_url(self):
        return reverse("chamran:home")

class FeedBack(models.Model):
    email       = models.EmailField(max_length=254, null=True, blank=True)
    opinion     = models.CharField(max_length=1000)
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_type   = models.CharField(max_length=20)
    user_info   = models.CharField(max_length=100)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + " - " + str(self.time_create)
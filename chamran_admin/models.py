import os

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

import uuid

from ChamranTeamSite import settings


def upload_to(instance, file_name):
    return os.path.join(settings.MEDIA_ROOT, 'message_attachments', file_name)


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
    text = models.TextField(verbose_name="متن خبر")
    picture = models.ImageField(upload_to=None, verbose_name="تصویر خبر")
    attachment = models.FileField(upload_to=None, verbose_name="ضمیمه", blank=True, null=True)
    link = models.CharField(max_length=128, verbose_name="لینک خبر")
    writer = models.CharField(max_length=32, verbose_name="نویسنده")
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return 'news/' + self.link


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

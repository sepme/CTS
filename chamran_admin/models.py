from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

import uuid


class Message(models.Model):
    title = models.CharField(max_length=128, verbose_name="عنوان", default="بدون عنوان")
    text = models.TextField(verbose_name="متن پیام")

    MESSAGE_TYPES = (
        (0, "اطلاعیه"),
        (1, "اخطار"),
        (2, "پیشنهاد"),
    )

    type = models.IntegerField(default=0, choices=MESSAGE_TYPES, verbose_name="نوع")
    attachment = models.FileField(upload_to=None, verbose_name="ضمیمه")
    receiver = models.ManyToManyField(User, verbose_name="گیرندگان")

    def __str__(self):
        return self.title

    def get_user_messages(self, user_id):
        user_messages = Message.objects.filter(receiver=User.objects.get(id=user_id))
        return user_messages


class News(models.Model):
    title = models.CharField(max_length=128, verbose_name="عنوان", default="بدون عنوان")
    text = models.TextField(verbose_name="متن خبر")
    picture = models.ImageField(upload_to=None, verbose_name="تصویر خبر")
    attachment = models.FileField(upload_to=None, verbose_name="ضمیمه")
    link = models.CharField(max_length=128, verbose_name="لینک خبر")
    writer = models.CharField(max_length=32, verbose_name="نویسنده")
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return 'news/' + self.link


class TempUser(models.Model):
    pub_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    email = models.EmailField(max_length=254, unique=True)
    unique = models.UUIDField(unique=True, default=uuid.uuid4())
    CHOICE = (
        ('expert', 'Expert'),
        ('industry', 'Industry'),
        ('researcher', 'Researcher')
    )
    account_type = models.CharField(max_length=50, choices=CHOICE)

    class Meta:
        ordering = ["-pub_date", ]

    def __str__(self):
        return self.account_type + ' - ' + str(self.pk)

    def get_absolute_url(self):
        return reverse("chamran:home")

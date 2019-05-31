from django.urls import path, include
from . import views

urlpatterns = [
    path('' , views.index.as_view(), name="index"),
    path('userInfo/',views.userInfo.as_view() ,name="userInfo")
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('userInfo/', views.userInfo.as_view(), name="userInfo")
]
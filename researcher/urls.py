from django.urls import path
from . import views

app_name = 'researcher'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('signup/<slug:username>', views.signup, name='signup'),
    path('messages/', views.Messages.as_view(), name="messages"),
]

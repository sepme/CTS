from django.urls import path
from . import views

app_name = 'researcher'
urlpatterns = [
    path('<int:pk>', views.Index.as_view() ,name='index'),
    path('userInfo/', views.userInfo.as_view(), name="userInfo"),
    path('login', views.Login.as_view()),
    path('userpass', views.UserPass.as_view()),
    path('signup/<slug:username>', views.signup, name='signup'),
]

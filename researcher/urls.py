from django.urls import path
from . import views

app_name='researcher'
urlpatterns = [
    path('' ,views.index.as_view()),
    path('login' ,views.login.as_view()),
    path('userpass' ,views.user_pass.as_view()),
    path('signup/<slug:username>' ,views.signup ,name='signup'),
]
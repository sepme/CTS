from django.urls import path, include

from . import views

app_name = 'chamran'

urlpatterns = [
    path('' ,views.Home.as_view() ,name='home'),
    path('signup/<str:account_type>/<uuid:code>' ,views.Signup_user.as_view() ,name='signup_username'),
    path('signup/' ,views.Signup_email.as_view() ,name='signup_email'),
]
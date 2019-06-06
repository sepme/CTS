from django.urls import path, include

from . import views

app_name = 'chamran'

urlpatterns = [
    path('' ,views.Home.as_view() ,name='home'),
    path('login/' ,views.LoginView.as_view() ,name='login'),
    path('logout/' ,views.LogoutView.as_view() ,name='logout'),
    path('signup/<str:account_type>/<uuid:code>' ,views.SignupUser.as_view() ,name='signup_username'),
    path('signup/' ,views.SignupEmail.as_view() ,name='signup_email'),
    path('resetpassword/' ,views.ResetPassword.as_view() ,name='send_reset_email'),
    path('resetpassword/<uuid:code>/' ,views.ResetPasswordConfirm.as_view() ,name='reset_password'),
]
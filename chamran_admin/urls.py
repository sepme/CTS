from django.urls import path, include

from . import views

app_name = 'chamran'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('notFound/', views.notFound.as_view(), name='notFound'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('test/', views.View.as_view(), name='test'),
    path('login_ajax/', views.login_ajax, name='login_ajax'),
    path('userpass/', views.UserPass.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/<str:account_type>/<uuid:unique_id>', views.SignupUser.as_view(), name='signup_username'),
    path('signup/', views.signup_email_ajax, name='signup_email'),
    path('resetpassword/', views.ResetPassword.as_view(), name='send_reset_email'),
    path('resetpassword/<uuid:unique_id>/', views.ResetPasswordConfirm.as_view(), name='reset_password'),
    path('recover_password/', views.RecoverPassword.as_view(), name='recover_password'),
    path('recover_password_ajax/', views.RecoverPassword_ajax, name="recovery_ajax"),
    path('recover_password/<uuid:unique_id>/', views.RecoverPasswordConfirm.as_view(), name='recover_password_confirm'),
    path('message_detail/<int:message_id>/', views.get_message_detail, name='message_detail')

]

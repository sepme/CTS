from django.urls import path
from . import views
from chamran_admin import views as chamran_admin_views

app_name = 'researcher'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('signup/<slug:username>', views.signup, name='signup'),
    path('messages/', chamran_admin_views.MessagesView.as_view(), name="messages"),
    path('technique/', views.Technique.as_view(), name="technique"),
    path('question/', views.Question.as_view(), name="question"),
]

from django.urls import path
from . import views

app_name = 'expert'

urlpatterns = [
    path('', views.index, name="index"),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('researcher/', views.ResearcherRequest.as_view(), name="researcherRequest"),
    path('messages/', views.Messages.as_view(), name="messages"),
    path('test/', views.test, name="test"),
    path('questions/', views.Questions.as_view(), name="questions"),

]
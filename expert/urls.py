from django.urls import path
from . import views

app_name = 'expert'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('userInfo/', views.user_info, name="userInfo"),
    path('researcher/', views.ResearcherRequest.as_view(), name="researcherRequest"),
    path('messages/', views.Messages.as_view(), name="messages"),
]
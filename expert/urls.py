from django.urls import path
from . import views
from chamran_admin import views as chamran_admin_views

app_name = 'expert'

urlpatterns = [
    path('', views.index, name="index"),
    path('userInfo/', views.user_info, name="userInfo"),
    path('researcher/', views.ResearcherRequest.as_view(), name="researcherRequest"),
    path('messages/', chamran_admin_views.MessagesView.as_view(), name="messages"),
    path('questions/', views.Questions.as_view(), name="questions"),
    path('scientific/', views.ajax_view, name="questions"),

]


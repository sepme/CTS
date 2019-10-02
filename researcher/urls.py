from django.urls import path
from . import views

app_name = 'researcher'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('signup/<slug:username>', views.signup, name='signup'),
    path('messages/', views.Messages.as_view(), name="messages"),
    path('technique/', views.Technique.as_view(), name="technique"),
    path('question/', views.Question.as_view(), name="question"),
    path('scientific_form/' ,views.ajax_ScientificRecord ,name='scientific_form'),
    path('executive_form/' ,views.ajax_ExecutiveRecord ,name='executive_form'),
    path('studious_form/' ,views.ajax_StudiousRecord ,name='studious_form'),
]

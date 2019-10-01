from django.urls import path
from . import views

app_name = 'expert'

urlpatterns = [
    path('', views.index, name="index"),
    path('userInfo/', views.user_info, name="userInfo"),
    path('researcher/', views.ResearcherRequest.as_view(), name="researcherRequest"),
    path('messages/', views.Messages.as_view(), name="messages"),
    path('questions/', views.Questions.as_view(), name="questions"),
    path('scientific/', views.scienfic_record_view, name="ajax_scientific"),
    path('executive/', views.executive_record_view, name="ajax_executive"),
    path('research/', views.research_record_view, name="ajax_research"),
    path('paper/', views.paper_record_view, name="ajax_paper"),

]


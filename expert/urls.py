from django.urls import path
from . import views
from chamran_admin import views as chamran_admin_views

app_name = 'expert'

urlpatterns = [
    path('', views.index, name="index"),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('researcher/', views.ResearcherRequest.as_view(), name="researcherRequest"),
    path('messages/', chamran_admin_views.MessagesView.as_view(), name="messages"),
    path('questions/', views.Questions.as_view(), name="questions"),
    path('scientific/', views.scienfic_record_view, name="ajax_scientific"),
    path('executive/', views.executive_record_view, name="ajax_executive"),
    path('research/', views.research_record_view, name="ajax_research"),
    path('paper/', views.paper_record_view, name="ajax_paper"),
    path('show_project/', views.show_project_view, name="show_project"),

]


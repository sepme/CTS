from django.urls import path
from . import views
from chamran_admin import views as chamran_admin_views

app_name = 'expert'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('researcher/', views.ResearcherRequest.as_view(), name="researcherRequest"),
    path('researcher/confirmResearcher/', views.confirmResearcher, name="confirm_researcher"),
    path('messages/', chamran_admin_views.MessagesView.as_view(), name="messages"),
    path('questions/', views.Questions.as_view(), name="questions"),
    path('scientific/', views.scienfic_record_view, name="ajax_scientific"),
    path('executive/', views.executive_record_view, name="ajax_executive"),
    path('research/', views.research_record_view, name="ajax_research"),
    path('paper/', views.paper_record_view, name="ajax_paper"),
    path('show_project/', views.show_project_view, name="show_project"),
    path('accept_project/', views.accept_project, name="accept_project"),
    path('new_research_question/', views.add_research_question, name="new_research_question"),
    path('show_research_question/', views.show_research_question, name="show_research_question"),
    path('terminate_research_question/', views.terminate_research_question, name="terminate_research_question"),
    path('set_answer_situation/', views.set_answer_situation, name="set_answer_situation"),
    path('show_researcher_preview/', views.show_researcher_preview, name="show_researcher_preview"),
    path('researcher_comment/', views.CommentForResearcher, name="researcher_comment"),
    path('industry_comment/', views.CommentForIndustry, name="industry_comment"),
    path('show_technique/', views.ShowTechnique, name="show-technique"),
    path('get_resume/', views.GetResume, name="get-resume"),
    path("active/", views.ActiveProjcet),
]


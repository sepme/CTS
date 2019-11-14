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
    path('show_technique/' ,views.ShowTechnique ,name="show_technique"),
    path('add_technique/' ,views.AddTechnique ,name="add_technique"),
    path('technique_review/', views.ajax_Technique_review, name="technique-review"),
    path('question/', views.Question.as_view(), name="question-alert"),
    path('question/<uuid:question_id>', views.QuestionShow.as_view(), name="question-show"),
    path('scientific_form/' ,views.ajax_ScientificRecord ,name='scientific_form'),
    path('executive_form/' ,views.ajax_ExecutiveRecord ,name='executive_form'),
    path('studious_form/' ,views.ajax_StudiousRecord ,name='studious_form'),
    path('show_project/' ,views.show_project_ajax ,name='show_project'),
    path('applyProject/' ,views.ApplyProject, name="apply_project"),
    path('comment/' ,views.AddComment ,name='comment'),
    path('myProject/' ,views.MyProject ,name="my_project"),
    path('doneProject/' ,views.DoneProjects ,name="done_project"),
]

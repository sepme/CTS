from django.urls import path
from . import views
from chamran_admin import views as chamran_admin_views

app_name = 'industry'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('show_project/', views.show_project_ajax, name='show_project'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('newProject/', views.NewProject.as_view(), name="newProject"),
    path('project_list/', views.ProjectListView.as_view(), name='project_list'),
    path('messages/', chamran_admin_views.MessagesView.as_view(), name="messages"),
    path('get_comment/', views.GetComment),
    path('accept_request/', views.accept_project),
    path('refuse_request/', views.refuse_expert),
    path("search_user_id", views.searchUserId, name="searchUserId"),
    path("project/<uuid:code>", views.showActiveProject.as_view(), name="show_active_project"),
    path("project-setting/", views.ProjectSetting, name="project-setting"),
    path("request_researcher/", views.industryRequestResearcher, name="request_researcher"),
    path("delete_researcher/", views.deleteResearcher, name="deleteResearcher"),
    path("confirm_researcher/", views.confirmResearcher, name="confirmResearcher"),
    path("reject_researcher/", views.rejectResearcher, name="rejectResearcher"),
]

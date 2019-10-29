from django.urls import path
from . import views
from chamran_admin import views as chamran_admin_views

app_name = 'industry'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('show_project/', views.show_project_ajax, name='show_project'),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('newProject/', views.NewProject.as_view(), name="newProject"),
    path('project_list/', views.ProjectListView.as_view(), name='project_list'),
    path('messages/', chamran_admin_views.MessagesView.as_view(), name="messages"),
]

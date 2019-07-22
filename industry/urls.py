from django.urls import path
from . import views

app_name = 'industry'

urlpatterns = [
    path('', views.Index.as_view() ,name='index'),
    path('userInfo/', views.userInfo.as_view(), name="userInfo"),
    path('newProject/', views.newProject.as_view(), name="newProject"),
    path('project_list/', views.ProjectListView.as_view() ,name='project_list'),
]

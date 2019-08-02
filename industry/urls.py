from django.urls import path
from . import views

app_name = 'industry'

urlpatterns = [
    path('<int:pk>/', views.Index.as_view(), name='index'),
    path('userInfo/', views.UserInfo.as_view(), name="userInfo"),
    path('newProject/', views.NewProject.as_view(), name="newProject"),
    path('project_list/', views.ProjectListView.as_view(), name='project_list'),
]

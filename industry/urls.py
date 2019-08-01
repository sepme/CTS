from django.urls import path
from . import views

app_name = 'industry'

urlpatterns = [
    path('<int:pk>/', views.Index.as_view() ,name='index'),
    path('userInfo/', views.userInfo.as_view(), name="userInfo"),
<<<<<<< HEAD
    path('newProject/', views.newProject.as_view(), name="newProject"),
    path('project_list/', views.ProjectListView.as_view() ,name='project_list'),
=======
    path('newProject/', views.newProject.as_view(), name="newProject")
>>>>>>> parent of a437e57... "Projects" Section Front-End + "Researcher Apply" Section Front-End
]

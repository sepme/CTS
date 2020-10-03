from django.urls import path

from . import views

app_name = 'bot_api'

urlpatterns = [
    path('project_name/<uuid:project_id>', views.projectName , name='projectName'),
    path('search_username/<str:keyword>', views.searchUsername , name='searchUsername'),
]

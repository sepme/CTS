from django.urls import path

from . import views
from . import reminder

app_name = 'bot_api'

urlpatterns = [
    # path('project_name/<str:project_id>', views.projectName , name='projectName'),
    # path('search_username/<str:keyword>', views.searchUsername , name='searchUsername'),

    path("", views.telegramHandler, name="telegramHandler"),
    path("get_webhook_info/", views.get_Webhook_info, name="get_webhook_info"),
    path("set_webhook/", views.set_webhook, name="set_webhook"),
    path("reminder/", reminder.reminder, name="reminder"),
    
]

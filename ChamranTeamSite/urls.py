from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('expert', include('expert.urls')),
    path('researcher', include('researcher.urls')),
    path('industry', include('industry.urls')),
]

urlpatterns += [
       path('accounts/', include('django.contrib.auth.urls')),
]
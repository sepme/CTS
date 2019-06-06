from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,include('chamran_admin.urls')),
    path('expert/', include('expert.urls')),
    path('researcher/', include('researcher.urls')),
    path('industry/', include('industry.urls')),
    # path('', include('django.contrib.auth.urls')),
]

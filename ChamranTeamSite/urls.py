from django.conf.urls.static import static
from django.conf.urls import handler404 ,handler500 ,handler403
from django.contrib import admin
from django.urls import path, include
from . import settings
from chamran_admin import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('react/', TemplateView.as_view(template_name="build/index.html")),
    path('', include('chamran_admin.urls')),
    path('expert/', include('expert.urls')),
    path('researcher/', include('researcher.urls')),
    path('industry/', include('industry.urls')),
    # path('', include('django.contrib.auth.urls')),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.notFound404
handler500 = views.notFound500
handler403 = views.Handler403
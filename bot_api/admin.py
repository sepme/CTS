from django.contrib import admin

from . import models

admin.site.register(models.NewGroup)
admin.site.register(models.Group)

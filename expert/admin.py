from django.contrib import admin

from . import models

@admin.register(models.ExpertUser)
class ExpertAdmin(admin.ModelAdmin):
    pass

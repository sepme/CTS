from django.contrib import admin

from . import models


@admin.register(models.ProjectForm)
@admin.register(models.IndustryUser)
class IndustryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IndustryForm)
class IndustryAdmin(admin.ModelAdmin):
    pass

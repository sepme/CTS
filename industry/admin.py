from django.contrib import admin

from . import models
# Register your models here.
@admin.register(models.IndustryUser)
class IdustryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.IndustryForm)
class IndustryFormAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProjectForm)
class ProjectFormAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
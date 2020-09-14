from django.contrib import admin

from . import models


@admin.register(models.Comment)
@admin.register(models.ProjectForm)
@admin.register(models.ResearchProjectForm)
@admin.register(models.Project)
@admin.register(models.ProjectHistory)
@admin.register(models.Keyword)
@admin.register(models.IndustryForm)
@admin.register(models.RandDProfile)
@admin.register(models.ResearchGroupProfile)
@admin.register(models.IndustryUser)
@admin.register(models.ExpertEvaluateIndustry)
@admin.register(models.InterfacePerson)
class IndustryAdmin(admin.ModelAdmin):
    pass

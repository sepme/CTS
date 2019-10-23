from django.contrib import admin
from . import models


@admin.register(models.ResearcherUser)
class ResearcherAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ResearcherProfile)
class ResearcherProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Status)

@admin.register(models.ScientificRecord)
class ScientificRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ExecutiveRecord)
class ExecutiveRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StudiousRecord)
class StudiousRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ResearchQuestionInstance)
class ResearchQuestionInstanceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Technique)
class TechniqueAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TechniqueInstance)
class TechniqueInstanceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TechniqueReview)
class TechniqueReviewAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from . import models

@admin.register(models.Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    pass
    
@admin.register(models.Researcher_profile)
class Researcher_profileAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from . import models


@admin.register(models.ResearcherUser)
class ResearcherAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ResearcherProfile)
class ResearcherProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Status)

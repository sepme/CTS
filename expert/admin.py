from django.contrib import admin

from . import models


@admin.register(models.ExpertUser)
class ExpertAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.ExpertForm)
admin.site.register(models.ScientificRecord)
admin.site.register(models.ExecutiveRecord)
admin.site.register(models.EqTest)
admin.site.register(models.ResearchQuestion)

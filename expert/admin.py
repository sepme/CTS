from django.contrib import admin

from . import models


@admin.register(models.ExpertUser)
class ExpertAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.ExpertForm)
admin.site.register(models.ScientificRecord)
admin.site.register(models.ExecutiveRecord)
admin.site.register(models.ResearchRecord)
admin.site.register(models.PaperRecord)
admin.site.register(models.EqTest)
admin.site.register(models.ResearchQuestion)
admin.site.register(models.ExpertRequestedProject)
admin.site.register(models.RequestResearcher)

admin.site.register(models.TempExpertForm)

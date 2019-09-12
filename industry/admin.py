from django.contrib import admin

from . import models
# Register your models here.
@admin.register(models.IndustryUser)
class IndustryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.IndustryForm)
class IdustryAdmin(admin.ModelAdmin):
    pass
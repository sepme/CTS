from django.contrib import admin

from . import models
# Register your models here.
@admin.register(models.IndustryUser)
class IdustryAdmin(admin.ModelAdmin):
    pass
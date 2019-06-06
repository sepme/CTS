from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.TempUser)
class TempUser(admin.ModelAdmin):
    pass

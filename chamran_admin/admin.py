from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.Temp_user)
class Temp_user(admin.ModelAdmin):
    pass
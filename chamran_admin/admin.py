from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Message)
@admin.register(models.TempUser)
class TempUser(admin.ModelAdmin):
    pass

@admin.register(models.News)
class News(admin.ModelAdmin):
    pass

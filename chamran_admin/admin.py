from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Message)
@admin.register(models.TempUser)
class TempUser(admin.ModelAdmin):
    pass


class Picture(admin.StackedInline):
    model = models.Picture
    extra = 1


@admin.register(models.News)
class News(admin.ModelAdmin):
    inlines = [
        Picture,
    ]


admin.site.register(models.FeedBack)

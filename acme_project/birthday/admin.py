from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag')
    list_edittable = ('tag')


admin.site.register(Tag)

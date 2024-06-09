from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import  Categories



class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_preview')
    search_fields = ('name',)
    list_filter = ('name',)

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
        else:
            return "No Image"

    photo_preview.short_description = 'Photo'

admin.site.register(Categories, CategoriesAdmin)


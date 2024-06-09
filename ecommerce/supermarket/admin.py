from django.contrib import admin
from .models import SuperMarket
from django.utils.safestring import mark_safe


# Register your models here.




class SuperMarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'localisation', 'photo_preview')
    search_fields = ('name', 'localisation')
    list_filter = ('name', 'localisation')

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
        else:
            return "No Image"

    photo_preview.short_description = 'Photo'

admin.site.register(SuperMarket, SuperMarketAdmin)

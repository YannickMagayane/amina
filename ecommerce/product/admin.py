from django.contrib import admin
from .models import Products
from django.utils.safestring import mark_safe


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'categories', 'supermarket', 'prix', 'photo_preview','marque','modele')
    search_fields = ('name', 'description', 'categories__name', 'supermarket__name','marque','modele')
    list_filter = ('categories', 'supermarket', 'prix','marque','modele')

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
        else:
            return "No Image"

    photo_preview.short_description = 'Photo'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('categories', 'supermarket')

    
admin.site.register(Products, ProductsAdmin)

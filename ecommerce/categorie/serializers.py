from rest_framework import serializers
from .models import Categories

class CategoriesSerializer(serializers.ModelSerializer):
    photo_svg = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ['name', 'photo', 'photo_svg']

    def get_photo_svg(self, obj):
        return obj.photo_to_svg()

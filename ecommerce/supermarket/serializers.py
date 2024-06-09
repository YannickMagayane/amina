from rest_framework import serializers
from .models import SuperMarket

class SuperMarketSerializer(serializers.ModelSerializer):
    photo_no_bg = serializers.SerializerMethodField()

    class Meta:
        model = SuperMarket
        fields = ['user', 'name', 'localisation', 'photo', 'photo_no_bg']

    def get_photo_no_bg(self, obj):
        return obj.remove_background()



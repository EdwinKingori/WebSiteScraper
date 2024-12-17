from rest_framework import serializers
from scrape_site.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'name', 'address']

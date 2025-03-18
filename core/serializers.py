from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['id', 'long_url', 'short_url', 'created_at', 'last_accessed', 'access_count', 'is_active']
        read_only_fields = ['short_url', 'created_at', 'last_accessed', 'access_count']

    def validate_long_url(self, value):
        """Validate the long_url field"""
        if len(value) > 2048:
            raise serializers.ValidationError("URL length exceeds maximum allowed length of 2048 characters.")
        return value
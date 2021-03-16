from rest_framework import serializers

from email_checker.models import APIEmail


class APIEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = APIEmail
        fields = (
            'email',
            'valid',
            'accessible',
            'catchall',
        )

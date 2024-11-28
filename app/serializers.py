from rest_framework import serializers
from .models import CtfWriteup
from datetime import datetime

class CtfWriteupSerializer(serializers.ModelSerializer):
    date = serializers.DateField(default=datetime.now().strftime("%Y-%m-%d"))

    class Meta:
        model = CtfWriteup
        fields = [
            "name",
            "category",
            "competition",
            "point_count",
            "description",
            "tags",
            "hints",
            "author",
            "markdown_body",
            "date",
        ]

    def create(self, validated_data):
        return CtfWriteup.objects.create_writeup(**validated_data)


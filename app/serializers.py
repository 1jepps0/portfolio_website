from rest_framework import serializers
from .models import CtfWriteup, CtfImage
from datetime import datetime


class CtfWriteupSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),  # Handle multiple image uploads
        required=False
    )

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
            "images"
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        writeup = CtfWriteup.objects.create(**validated_data)

        for image in images_data:
            CtfImage.objects.create(writeup=writeup, image=image)

        return writeup 


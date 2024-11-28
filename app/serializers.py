from rest_framework import serializers
from .models import CtfWriteup, CtfImage
from datetime import datetime

class CtfImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CtfImage
        fields = ['image']

class CtfWriteupSerializer(serializers.ModelSerializer):
    date = serializers.DateField(default=datetime.now().strftime("%Y-%m-%d"))
    images = CtfImageSerializer(many=True, write_only=True)  # Accept multiple images

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
        print("create")
        images_data = validated_data.pop('images', [])
        writeup = CtfWriteup.objects.create_writeup(**validated_data)

        for image_data in images_data:
            CtfImage.objects.create(writeup=writeup, **image_data)

        return writeup


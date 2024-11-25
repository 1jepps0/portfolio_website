from django.db import models

# Create your models here.

class CtfWriteup(models.Model):
    name = models.CharField(max_length = 50)
    category = models.CharField(max_length = 50)
    competetion = models.CharField(max_length = 50)
    point_count = models.IntegerField()
    description = models.TextField()
    tags = models.CharField(max_length = 300)
    hints = models.CharField(max_length = 300)

    author = models.CharField(max_length = 50, blank = True, null = True)
    markdown_body = models.TextField(default="")
    image = models.ImageField()


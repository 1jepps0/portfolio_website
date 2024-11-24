from django.db import models

# Create your models here.

class CtfWriteup(models.Model):
    name = models.CharField(max_length = 50)
    competetion = models.CharField(max_length = 50)
    point_count = models.IntegerField()
    description = models.CharField(max_length = 500)
    tags = models.CharField(max_length = 300)
    hints = models.CharField(max_length = 300)

    author = models.CharField(max_length = 50, blank = True, null = True)

    body_text = models.CharField(max_length = 5000, default="")
    code_snippets = models.CharField(max_length = 5000, default="")

    image = models.ImageField()


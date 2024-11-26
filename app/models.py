from django.db import models

# Create your models here.

class CtfWriteup(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    competition = models.CharField(max_length=50)
    point_count = models.IntegerField()
    description = models.TextField()
    tags = models.CharField(max_length=300)
    hints = models.CharField(max_length=300)
    date = models.DateField()

    author = models.CharField(max_length=50, blank=True, null=True)
    markdown_body = models.FileField(upload_to="writeups")

    def __str__(self):
        return self.name


class CtfImage(models.Model):
    writeup = models.ForeignKey(CtfWriteup, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="writeup_images")

    def __str__(self):
        return f"Image for {self.writeup.name}"

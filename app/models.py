from django.db import models
import datetime

class WriteupManager(models.Manager):
    def create_writeup(self, name, category, competition, point_count,
                       description, tags, hints, date, author, markdown_body):

        CtfWriteup = self.create(name=name, category=category, competition=competition,
                                 point_count=point_count, description=description,
                                 tags=tags, hints=hints, date=date, author=author,
                                 markdown_body=markdown_body)
        return CtfWriteup



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
    markdown_body = models.TextField()

    objects = WriteupManager()

    def __str__(self):
        return self.name

class CtfImage(models.Model):
    writeup = models.ForeignKey(CtfWriteup, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="writeup_images")

    def __str__(self):
        return f"Image for {self.writeup.name}"

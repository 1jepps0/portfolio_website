import datetime
import os

from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from django.utils.text import slugify

def writeup_image_upload_path(instance, filename):
    competition = slugify(instance.writeup.competition)
    name = slugify(instance.writeup.name)
    return os.path.join("writeup_images", competition, name, filename)


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
    image = models.ImageField(upload_to=writeup_image_upload_path)

    def __str__(self):
        return f"Image for {self.writeup.name}"




""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)

""" Delete the file if something else gets uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            # It's got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)

""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model, instance, field, instance_file_field):
    if not instance_file_field:
        return

    dynamic_field = {field.name: instance_file_field.name}
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()

    if not other_refs_exist:
        file_path = instance_file_field.path
        instance_file_field.delete(False)  # Delete the file but not the reference
        delete_empty_folder(file_path)

""" Delete the folder if it's empty and its parent folder if it's also empty """
def delete_empty_folder(file_path):
    folder_path = os.path.dirname(file_path)           # The folder containing the file
    parent_folder_path = os.path.dirname(folder_path)  # The parent of the folder

    try:
        # Delete the folder if it's empty
        if folder_path and not os.listdir(folder_path):
            os.rmdir(folder_path)

        # Delete the parent folder if it's empty (after the folder has been deleted)
        if parent_folder_path and not os.listdir(parent_folder_path):
            os.rmdir(parent_folder_path)

    except (FileNotFoundError, OSError):
        pass  # Folder either doesn't exist or isn't empty; no action needed

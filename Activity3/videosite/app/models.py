import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class Video(models.Model):
    """ Stores information about the video in the database. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=200)
    views = models.IntegerField()
    owner = models.ForeignKey(User, models.CASCADE)
    file = models.FileField(upload_to='videos/%Y/%m/%d', null=True)


@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

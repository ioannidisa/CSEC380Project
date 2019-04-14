# Generated by Django 2.1.7 on 2019-04-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='file_name',
        ),
        migrations.AddField(
            model_name='video',
            name='file',
            field=models.FileField(null=True, upload_to='videos/%Y/%m/%d'),
        ),
    ]
# Generated by Django 2.2.4 on 2019-08-28 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20190828_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='blog/%Y/%m/%d'),
        ),
    ]
# Generated by Django 4.1.2 on 2022-10-31 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mydictionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videocategory',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
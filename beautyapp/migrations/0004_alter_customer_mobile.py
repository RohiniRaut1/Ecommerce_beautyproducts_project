# Generated by Django 5.0.6 on 2024-05-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beautyapp', '0003_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.IntegerField(),
        ),
    ]
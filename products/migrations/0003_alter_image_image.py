# Generated by Django 4.2 on 2023-04-26 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_apertment_is_fur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='Image',
            field=models.CharField(max_length=2000),
        ),
    ]

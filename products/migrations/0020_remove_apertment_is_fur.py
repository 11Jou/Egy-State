# Generated by Django 4.2 on 2023-04-27 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_apertment_is_fur_alter_apertment_apertment_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apertment',
            name='is_fur',
        ),
    ]
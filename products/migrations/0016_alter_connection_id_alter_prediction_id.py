# Generated by Django 4.2 on 2023-04-26 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_apertment_id_alter_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='id',
            field=models.IntegerField(default=1, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='id',
            field=models.IntegerField(default=1, max_length=50, primary_key=True, serialize=False),
        ),
    ]

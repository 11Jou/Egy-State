# Generated by Django 4.2 on 2023-04-26 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_apertment_apertment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='apertment',
            name='id',
            field=models.BigAutoField(auto_created=True, default=' ', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apertment',
            name='Apertment_Id',
            field=models.CharField(max_length=50),
        ),
    ]

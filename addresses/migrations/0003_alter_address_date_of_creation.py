# Generated by Django 4.2.7 on 2024-04-22 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_address_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='date_of_creation',
            field=models.DateField(blank=True, help_text='В формате "дд.мм.гггг"', null=True, verbose_name='Дата создания'),
        ),
    ]

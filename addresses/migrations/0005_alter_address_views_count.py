# Generated by Django 4.2.7 on 2024-05-05 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_alter_address_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='views_count',
            field=models.IntegerField(default=0, editable=False, verbose_name='просмотры'),
        ),
    ]
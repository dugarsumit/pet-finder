# Generated by Django 2.2 on 2019-05-11 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0012_detail_enabled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='pet_id',
            new_name='pet',
        ),
        migrations.RenameField(
            model_name='query',
            old_name='pet_id',
            new_name='pet',
        ),
    ]

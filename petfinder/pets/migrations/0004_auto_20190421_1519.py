# Generated by Django 2.2 on 2019-04-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_detail_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='mobile',
            field=models.CharField(max_length=15),
        ),
    ]

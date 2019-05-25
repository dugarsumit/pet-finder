# Generated by Django 2.2 on 2019-05-25 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0013_auto_20190511_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='age_month',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='age_year',
        ),
        migrations.AddField(
            model_name='detail',
            name='age',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='detail',
            name='species',
            field=models.CharField(choices=[('Dog', 'Dog'), ('Cat', 'Cat')], default='Dog', max_length=100),
        ),
    ]

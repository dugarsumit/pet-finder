# Generated by Django 2.2 on 2019-08-24 12:50

from django.db import migrations
import django_countries.fields
import pets.models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0022_auto_20190824_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='forbidden_countries',
            field=pets.models.MultipleCountryField(base_field=django_countries.fields.CountryField(blank=True, max_length=2, null=True), db_index=True, help_text='Specify countries in which adoptions of this pet is not allowed. (Hold down the Ctrl (windows) / Command (Mac) button to select multiple options.)', null=True, size=None),
        ),
    ]
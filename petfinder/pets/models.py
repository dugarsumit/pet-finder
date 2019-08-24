from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django import forms
from django_countries import countries

class MultipleCountryField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(models.CharField(max_length=...,
                                                    choices=(...,)),
                                   default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


# Create your models here.

class Detail(models.Model):
    id = models.AutoField(primary_key = True, db_index = True)
    age = models.FloatField(default = 0.0, db_index = True)
    dob = models.CharField(max_length = 100, null = True)
    breed = models.CharField(max_length = 500, null = True, db_index = True)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now = True, db_index = True)
    city = models.CharField(max_length = 250, null = True, db_index = True)
    country = CountryField(null = True)
    story = models.TextField(null = True, help_text = 'Write a story about the pet')
    sterilized = models.BooleanField(default = False, db_index = True)
    house_trained = models.BooleanField(default = False, db_index = True)
    is_adopted = models.BooleanField(default = False, db_index = True)
    show_badge = models.BooleanField(default = False)
    characteristics = models.TextField(null = True,
                                       help_text = 'Specify pet traits such as - Curious, Handsome, Playful, Loves Treats, Clever, Gold eyes.',
                                       db_index = True)
    name = models.CharField(max_length = 100, null = False)
    gender = models.CharField(max_length = 10, choices = (('M', 'Male'), ('F', 'Female')), default = 'M')
    email = models.CharField(max_length = 100, null = False)
    mobile = models.CharField(max_length = 15, null = False)
    added_by = models.ForeignKey(User, on_delete = models.CASCADE)
    peepalfarm_approved = models.BooleanField(default = False)
    enabled = models.BooleanField(default = False)
    species = models.CharField(max_length = 100, choices = (('Dog', 'Dog'), ('Cat', 'Cat')), default = 'Dog')
    hair_length = models.CharField(max_length = 100,
                                   choices = (('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')),
                                   default = 'Medium')
    size = models.CharField(max_length = 100,
                            choices = (
                                ('Small', 'Small (1-10kg)'), ('Medium', 'Medium (10-20kg)'),
                                ('Large', 'Large (20-30kg)'), ('X-Large', 'X-Large (30+ kg)')),
                            default = 'Medium')
    kid_friendly = models.BooleanField(default = False)
    cat_friendly = models.BooleanField(default = False)
    dog_friendly = models.BooleanField(default = False)
    special_needs = models.BooleanField(default = False)
    forbidden_countries = MultipleCountryField(models.CharField(max_length = 2, null = True, blank = True, choices = tuple(countries)),
                                               help_text = 'Specify countries in which adoptions of pet is not allowed. (Hold down the Ctrl (windows) / Command (Mac) button to select multiple options.)',
                                               db_index = True,
                                               null = True,
                                               blank = True)

class Media(models.Model):
    id = models.AutoField(primary_key = True, db_index = True)
    pet = models.ForeignKey(Detail, on_delete = models.CASCADE)
    type = models.CharField(max_length = 50, choices = (('image', 'image'), ('video', 'video')))
    is_thumbnail = models.BooleanField(default = False)
    path = models.CharField(max_length = 250)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now = True, db_index = True)


class Query(models.Model):
    id = models.AutoField(primary_key = True, db_index = True)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now = True, db_index = True)
    type = models.CharField(max_length = 50, choices = (('G', 'General'), ('A', 'Adoption')), db_index = True,
                            default = 'G')
    email = models.CharField(max_length = 100, null = False)
    mobile = models.CharField(max_length = 15, null = False)
    query = models.TextField(null = True)
    location = models.CharField(max_length = 250, null = True, db_index = True)
    name = models.CharField(max_length = 100, null = False)
    pet = models.ForeignKey(Detail, on_delete = models.SET_NULL, null = True)
    pet_name = models.CharField(max_length = 100, null = True)
    is_adopted = models.BooleanField(default = False)

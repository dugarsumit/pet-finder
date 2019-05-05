from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


# Create your models here.

class Detail(models.Model):
    id = models.AutoField(primary_key = True, db_index = True)
    age_month = models.IntegerField(default = 0)
    age_year = models.BigIntegerField(default = 0, db_index = True)
    breed = models.CharField(max_length = 500, null = True, db_index = True)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now = True, db_index = True)
    # location = models.CharField(max_length = 250, null = True, db_index = True)
    city = models.CharField(max_length = 250, null = True, db_index = True)
    # state = models.CharField(max_length = 250, null = True, db_index = True)
    country = CountryField(null = True)
    story = models.TextField(null = True, help_text = 'Write a story about the pet')
    sterilized = models.BooleanField(default = False, db_index = True)
    house_trained = models.BooleanField(default = False, db_index = True)
    is_adopted = models.BooleanField(default = False, db_index = True)
    show_badge = models.BooleanField(default = False)
    characteristics = models.TextField(null = True,
                                       help_text = 'Specify pet traits such as - Curious, Handsome, Playful, Loves Treats, Clever, Gold eyes, Medium length fur',
                                       db_index = True)
    name = models.CharField(max_length = 100, null = False)
    gender = models.CharField(max_length = 10, choices = (('M', 'Male'), ('F', 'Female')), default = 'M')
    email = models.CharField(max_length = 100, null = False)
    mobile = models.CharField(max_length = 15, null = False)
    added_by = models.ForeignKey(User, on_delete = models.CASCADE)
    peepalfarm_approved = models.BooleanField(default = False)


class Media(models.Model):
    id = models.AutoField(primary_key = True, db_index = True)
    pet_id = models.ForeignKey(Detail, on_delete = models.CASCADE)
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
    pet_id = models.ForeignKey(Detail, on_delete = models.SET_NULL, null = True)
    pet_name = models.CharField(max_length = 100, null = True)
    is_adopted = models.BooleanField(default = False)

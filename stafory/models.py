import datetime

from django.db import models
from django.core.exceptions import ValidationError
from .settings import GENDER_CHOICES


class Child(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    pic = models.ImageField(upload_to='children/', blank=True, null=True)  # ideally + size validator
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=True)
    birth_date = models.DateField()
    form = models.SmallIntegerField(null=True)  # 1, 2..
    group = models.CharField(max_length=1, null=True)  # A, B, C..
    is_studying = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def validate_studying_child(value):
    if not value.is_studying:
        raise ValidationError('Child is not studying')


class Journal(models.Model):
    id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, validators=[validate_studying_child])
    # ideally we need new model Trustee with relation who can take particular child
    # and here should be relation to Trustee
    trustee_name = models.CharField(max_length=200)
    arrived_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)





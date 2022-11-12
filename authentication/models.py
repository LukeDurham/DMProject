from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

currentyear = datetime.datetime.now().year + 1
class Meta:

    app_label = 'yourApp'
def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Users(models.Model):
    EmployeeAccess = (
        ('A', 'Admin'),
        ('E', 'Employee'),
        ('M', 'Manager')
    )
    Username = models.CharField(max_length=12, primary_key=True)
    Password = models.CharField(max_length=20)
    Email = models.CharField(max_length=20)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    AccessLevel = models.CharField(max_length=1, choices=EmployeeAccess)


class Vehicle(models.Model):
    statusOptions = (
         ('L', 'Lot'),
         ('D', 'Detail'),
         ('S', 'Service')
     )
    CarID = models.CharField(max_length=12, primary_key=True)
    year = models.IntegerField(validators=[MinValueValidator(1930), MaxValueValidator(currentyear)])
    make = models.CharField(max_length=30, null=False)
    model = models.CharField(max_length=20, null=False)
    miles = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1500000)])
    color = models.CharField(max_length=15)
    location = models.CharField(max_length=30, null=False)
    status = models.CharField(max_length=1, choices=statusOptions, null=False)
    DateAdded = models.DateField()
class Meta:
    app_label = 'user_app'



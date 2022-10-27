from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

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
    year = models.CharField(max_length=4)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=255)
    miles = models.CharField(max_length=7)
    color = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=statusOptions)
class Meta:
    app_label = 'user_app'



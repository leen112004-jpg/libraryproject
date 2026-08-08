from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)

class Address(models.Model):
    city = models.CharField(max_length=50)

class Card(models.Model):
    card_number = models.IntegerField()


class Department(models.Model):
    name = models.CharField(max_length=50)

class Course(models.Model):
    title = models.CharField(max_length=50)
    code = models.IntegerField()

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    card = models.OneToOneField(Card, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)  

class Address(models.Model):
    city = models.CharField(max_length=100)

class Student(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Address2(models.Model):
    city = models.CharField(max_length=100)

class Student2(models.Model):
    name = models.CharField(max_length=100)
    addresses = models.ManyToManyField(Address2)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/')
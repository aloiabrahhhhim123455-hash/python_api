from django.db import models

# Create your models here.
class login (models.Model):
    username = models.CharField(max_length=50)
    passwored = models.CharField(max_length=50)


    def __str__(self):
        return self.username
    

class product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

class student (models.Model):
    nu = models.IntegerField()
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    adress = models.CharField()



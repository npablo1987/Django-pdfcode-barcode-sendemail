from django.db import models

# Create your models here.

class Alumnos(models.Model):
    rut = models.CharField(max_length=15)
    nombre = models.CharField(max_length=50)
    apellidop = models.CharField(max_length=50)
    apellidom =  models.CharField(max_length=50)
    email = models.EmailField()
    telefono =  models.IntegerField()

class Modulos(models.Model):
    nombremodulo = models.CharField(max_length=50)
    carrera = models.CharField(max_length=50)
    docente = models.CharField(max_length=50)
    nhoras = models.IntegerField()

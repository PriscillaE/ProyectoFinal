from __future__ import unicode_literals
from django.core.validators import RegexValidator
from datetime import datetime, time, date, timedelta
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Donadores(models.Model):
    Donador_nombre=models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z\s]*$',message="Valor invalido")])
    Donador_correo=models.EmailField()
    Donador_tel=models.CharField(max_length=15,validators=[RegexValidator(regex='^[0-9|\\-]*$',message="Ingrese un numero de telefono valido")])

    def __unicode__(self):
        return " %s"%(self.Donador_nombre)

class Donaciones_Monetarias(models.Model):
    Donaciones_opciones=(
    ('CH','Cheque'),
    ('DE','Deposito'),
    ('EF','Efectivo'),
    )
    Fecha=models.DateField(default=date.today)
    Donador=models.ForeignKey(Donadores)
    Cantidad=models.DecimalField(max_digits=8,decimal_places=2)
    Forma_pago=models.CharField(max_length=15,choices=Donaciones_opciones)

    def __unicode__(self):
        return "Fecha: %s - Donador: %s"%(self.Fecha,self.Donador) 

class Donaciones_Especie(models.Model):
    Fecha=models.DateField(default=date.today)
    Donador=models.ForeignKey(Donadores)
    Descripcion=models.CharField(max_length=60)
    Unidades=models.CharField(max_length=20)
    Cantidad=models.IntegerField()

    def __unicode__(self):
        return "Fecha: %s - Donador: %s"%(self.Fecha,self.Donador) 
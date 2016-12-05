from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime, time, date, timedelta
from django.db import models
from Donadores.models import Donaciones_Monetarias, Donaciones_Especie
from Admon.models import Personal,Administradores,Minutas,Eventos
from django.contrib.auth.models import User

# Create your models here.

def validate_edad(date):
    nino=abs(date.today()-date)
    if (nino.days/360>=18):
        raise ValidationError("El paciente debe ser menor de edad")


class Paciente(models.Model):
    Estado_opciones=(
    ('RE','Remision'),
    ('TR','En Tratamiento'),
    ('DEP','Fallecido'),
    )
    Paciente_nombre=models.CharField(max_length=40,validators=[RegexValidator(regex='^[a-zA-Z\s]*$',message="Valor invalido")])
    Paciente_apellido=models.CharField(max_length=50,validators=[RegexValidator (regex='^[a-zA-Z\s]*$',message="Valor invalido")])
    Paciente_fnacimiento=models.DateField(validators=[validate_edad])
    Paciente_diagnostico=models.CharField(max_length=200)
    Paciente_clinica=models.CharField(max_length=50)
    Tutor_Padre=models.CharField(max_length=50)
    Paciente_contacto=models.CharField(max_length=15,validators=[RegexValidator(regex='^[0-9|\\-]*$',message="Ingrese un numero de telefono valido")])
    Estado_salud=models.CharField(max_length=10,choices=Estado_opciones)

    def __unicode__(self):
        return " %s  %s"%(self.Paciente_nombre,self.Paciente_apellido) 

class Historial_Medico(models.Model):
    Paciente_hm=models.ForeignKey(Paciente)
    Fecha=models.DateField(default=date.today)
    Diagnostico=models.TextField()

    def __unicode__(self):
        return "Paciente: %s - Fecha: %s"%(self.Paciente_hm,self.Fecha) 

class Seguimiento_Apoyo(models.Model):
    Apoyo_Paciente=models.ForeignKey(Paciente)
    Donacion_monetaria=models.DecimalField(max_digits=8,decimal_places=2,blank=True)
    Donacion_especie=models.TextField(blank=True)
    Fecha_entrega=models.DateField(default=date.today)

    def __unicode__(self):
        return "Paciente: %s - Fecha: %s"%(self.Apoyo_Paciente,self.Fecha_entrega) 

class Defunciones(models.Model):
    Paciente=models.ForeignKey(Paciente)
    Fecha_apoyo=models.DateField(default=date.today)
    Apoyo=models.DecimalField(max_digits=8,decimal_places=2)
    Recipiente_nombre=models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z\s]*$',message="Valor invalido")])

    def __unicode__(self):
        return " %s  %s"%(self.Paciente,self.Fecha_apoyo) 
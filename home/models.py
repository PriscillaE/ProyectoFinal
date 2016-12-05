from __future__ import unicode_literals
from datetime import datetime, time, date, timedelta
from django.db import models
from django.contrib.auth.models import User

# class Paciente(models.Model):
#     Estado_opciones=(
#     ('RE','Remision'),
#     ('TR','En Tratamiento'),
#     ('DEP','Fallecido'),
#     )
#     Paciente_nombre=models.CharField(max_length=40)
#     Paciente_apellido=models.CharField(max_length=50)
#     Paciente_fnacimiento=models.DateField()
#     Paciente_diagnostico=models.CharField(max_length=200)
#     Paciente_clinica=models.CharField(max_length=50)
#     Tutor_Padre=models.CharField(max_length=50)
#     Paciente_contacto=models.CharField(max_length=15,blank=True)
#     Estado_salud=models.CharField(max_length=10,choices=Estado_opciones)

#     def __unicode__(self):
#         return "Name: %s - Surname: %s"%(self.Paciente_nombre,self.Paciente_apellido) 


# class Historial_Medico(models.Model):
#     Paciente_hm=models.ForeignKey(Paciente)
#     Fecha=models.DateField(default=date.today)
#     Diagnostico=models.TextField()


# class Donadores(models.Model):
#     Donador_nombre=models.CharField(max_length=50)
#     Donador_correo=models.EmailField()
#     Donador_tel=models.CharField(max_length=15)


# class Donaciones_Monetarias(models.Model):
#     Donaciones_opciones=(
#     ('CH','Cheque'),
#     ('DE','Deposito'),
#     ('EF','Efectivo')
#     )
#     Fecha=models.DateField(default=date.today)
#     Donador=models.ForeignKey(Donadores)
#     Cantidad=models.IntegerField()
#     Forma_pago=models.CharField(max_length=15,choices=Donaciones_opciones)


# class Donaciones_Especie(models.Model):
#     Fecha=models.DateField(default=date.today)
#     Donador=models.ForeignKey(Donadores)
#     Descripcion=models.CharField(max_length=60)
#     Unidades=models.CharField(max_length=20)
#     Cantidad=models.IntegerField()


# class Seguimiento_Apoyo(models.Model):
#     Apoyo_Paciente=models.ForeignKey(Paciente)
#     Donacion_monetaria=models.ForeignKey(Donaciones_Monetarias,blank=True)
#     Donacion_especie=models.ForeignKey(Donaciones_Especie,blank=True)
#     Fecha_entrega=models.DateField(default=date.today)


# class Personal(models.Model):
#     Personal_nombre=models.CharField(max_length=40)
#     Personal_apellidos=models.CharField(max_length=50)
#     Personal_funcion=models.CharField(max_length=60)
#     Personal_tel=models.CharField(max_length=15)
#     Personal_correo=models.EmailField()

# class Administradores(models.Model):
#     perfil=models.OneToOneField(User)
#     Admon_nombre=models.CharField(max_length=40)
#     Admon_tel=models.CharField(max_length=15)
#     Admon_correo=models.EmailField()
#     class Meta:
#         permissions = (
#             ("editar", "Edicion de registros"),
#             )

# class Minutas(models.Model):
#     Fecha_reunion=models.DateField()
#     Asistentes=models.ManyToManyField(Administradores)
#     Total_donacionesmon=models.IntegerField()
#     Valor_donacionesesp=models.IntegerField()
#     Duracion_reunion=models.CharField(max_length=15)
#     Pacientes_beneficiados=models.IntegerField()
#     Observaciones=models.TextField()

# class Eventos(models.Model):
#     Fecha_evento=models.DateField()
#     Lugar_evento=models.CharField(max_length=100)
#     Personal_evento=models.ManyToManyField(Personal)
#     Hora_evento=models.TimeField()


# class Defunciones(models.Model):
#     Paciente=models.ForeignKey(Paciente)
#     Fecha_apoyo=models.DateField(default=date.today)
#     Apoyo=models.IntegerField()
#     Recipiente_nombre=models.CharField(max_length=50)


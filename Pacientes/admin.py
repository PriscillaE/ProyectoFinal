from django.contrib import admin

from .models import Paciente,Historial_Medico,Seguimiento_Apoyo,Defunciones



admin.site.register(Seguimiento_Apoyo)
admin.site.register(Historial_Medico)
admin.site.register(Paciente)
admin.site.register(Defunciones)


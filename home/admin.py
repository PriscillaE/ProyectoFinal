from django.contrib import admin
from .models import Paciente,Historial_Medico,Donadores,Donaciones_Monetarias,Donaciones_Especie,Seguimiento_Apoyo
from .models import Personal,Administradores,Eventos ,Minutas,Defunciones

admin.site.register(Paciente)
admin.site.register(Historial_Medico)
admin.site.register(Donaciones_Especie)
admin.site.register(Donadores)
admin.site.register(Donaciones_Monetarias)
admin.site.register(Seguimiento_Apoyo)
admin.site.register(Personal)
admin.site.register(Administradores)
admin.site.register(Minutas)
admin.site.register(Defunciones)


#administrador
#sepher123
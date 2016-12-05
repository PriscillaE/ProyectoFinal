from django.contrib import admin

from .models import Personal,Administradores,Eventos ,Minutas


admin.site.register(Personal)
admin.site.register(Administradores)
admin.site.register(Minutas)
admin.site.register(Eventos)


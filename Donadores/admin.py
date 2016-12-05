from django.contrib import admin
from .models import Donadores,Donaciones_Monetarias,Donaciones_Especie

admin.site.register(Donaciones_Especie)
admin.site.register(Donadores)
admin.site.register(Donaciones_Monetarias)

"""ProyectoSepher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from Admon.views import Index_view, Admin_view, Historia_view , Mision_view, Ubicacion_view ,Registro_Minutas, Editar_Minuta ,Detalle_minuta, Reporte_Minutas, Registro_Eventos, Eliminar_Eventos, Editar_Evento, Reporte_Eventos, Detalle_eventos, Registro_Personal, Editar_Personal, Reporte_Personal,Donar,Galeria,wsEventos, sephereventos, Personal_pdf
from Donadores.views import  Register_Donadores, Register_Donaciones_Monetarias, Register_Donaciones_Especie, donadores_report, donaciones_monetarias_report, donaciones_monetarias_report, donaciones_especie_report, Editar_Donador, EditarDonaciones_monetarias, Editar_Donaciones_especie, wsUltimoDonaciones,wsUltimoDefunciones,wsUltimoApoyo,ReporteMensual
from Pacientes.views import Registro_Apoyo, Reporte_Apoyo, Registro_Defunciones, Reporte_Defunciones, Registro_paciente, Detalle_Paciente_pdf
from Pacientes.views import Reporte_Paciente, EditarPaciente, Paciente_detalle, Registro_Historial,consulta, Defunciones_pdf, Pacientes_pdf, Apoyo_pdf
from Donadores.views import Don_monetarias_pdf,Mensual_pdf,Don_especie_pdf

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',login, {'template_name':'admin.html'},name='login'),
    url(r'^salir/$',logout_then_login,name='logout'),    
    url(r'^registro_paciente/$',Registro_paciente.as_view(),name='RegistroPac_view'),
    url(r'^reporte_pacientes/$',Reporte_Paciente.as_view(),name='reporte_pacientes'),
   	url(r'^editar_paciente/(?P<pk>\d+)$',EditarPaciente.as_view(),name='editar_paciente_view'),
   	url(r'^detalle_paciente/(?P<pk>\d+)$',Paciente_detalle,name='paciente_detalle_view'),
   	url(r'^registro_medico/$',Registro_Historial.as_view(),name='RegistroMed_view'),
   	url(r'^registro_minutas/$',Registro_Minutas.as_view(),name='RegistroMin_view'),
   	url(r'^detalle_minuta/(?P<pk>\d+)$',Detalle_minuta.as_view(),name='DetalleMin_view'),
   	url(r'^reporte_minutas/$',Reporte_Minutas.as_view(),name='ReporteMin_view'),
    url(r'^editar_minuta/(?P<pk>\d+)$',Editar_Minuta.as_view(),name='Editar_Minuta_view'),
   	url(r'^registro_defunciones/$',Registro_Defunciones.as_view(),name='RegistroDef_view'),
   	url(r'^registro_apoyo/$',Registro_Apoyo.as_view(),name='RegistroApy_view'),
   	url(r'^reporte_defunciones/$',Reporte_Defunciones.as_view(),name='ReporteDef_view'),
   	#rl(r'^eliminar_defunciones/(?P<pk>\d+)$',Reporte_Defunciones.as_view(),name='EliminarDef_view'),
   	url(r'^registro_eventos/$',Registro_Eventos.as_view(),name='RegitroEve_view'),
   	url(r'^eliminar_eventos/(?P<pk>\d+)$',Eliminar_Eventos.as_view(),name='EliminarEve_view'),
   	url(r'^editar_evento/(?P<pk>\d+)$',Editar_Evento.as_view(),name='editar_evento_view'),
   	url(r'^reporte_eventos/$',Reporte_Eventos.as_view(),name='ReporteEve_view'),
   	url(r'^detalle_evento/(?P<pk>\d+)$',Detalle_eventos.as_view(),name='DetalleEve_view'),
   	url(r'^registro_personal/$',Registro_Personal.as_view(),name='reporte_personal'),
   	#url(r'^eliminar_personal/(?P<pk>\d+)$',Eliminar_Personal.as_view(),name='EliminarPer_view'),
   	url(r'^editar_personal/(?P<pk>\d+)$',Editar_Personal.as_view(),name='editar_personal_view'),
   	url(r'^reporte_personal/$',Reporte_Personal.as_view(),name='ReportePer_view'),
    url(r'^Donadores_registro/$', Register_Donadores.as_view(), name = 'Register_Donadores'),
    url(r'^Donadores_monetarias_registro/$', Register_Donaciones_Monetarias.as_view(), name = 'Donadores_monetarias_register_view'),
    url(r'^Donadores_especie_registro/$', Register_Donaciones_Especie.as_view(), name = 'Donadores_especie_register_view'),
    url(r'^Donadores_editar/$', donadores_report.as_view(), name = 'Donadores_eliminar_view'),
    url(r'^Donaciones_monetarias_editar/$', donaciones_monetarias_report.as_view(), name = 'Donaciones_monetarias_eliminar_view'),\
    url(r'^Donaciones_especie_editar/$', donaciones_especie_report.as_view(), name = 'Donadores_especie_eliminar_view'),
    url(r'^editar_donador/(?P<pk>\d+)$',Editar_Donador.as_view(),name='eliminar_donador_view'),
    url(r'^editar_donaciones_monetarias/(?P<pk>\d+)$',EditarDonaciones_monetarias.as_view(),name='eliminar_donaciones_monetarias_view'),
    url(r'^editar_donaciones_especie/(?P<pk>\d+)$',Editar_Donaciones_especie.as_view(),name='eliminar_donaciones_especie_view'),
    url(r'^donar/$',Donar.as_view(),name='donar_view'),
    url(r'^galeria/$',Galeria.as_view(),name='galeria_view'),
    url(r'^Mision/$', Mision_view.as_view(), name = 'Mision_view'),
    url(r'^Historia/$', Historia_view.as_view(), name = 'Historia_view'),
    url(r'^Ubicacion/$', Ubicacion_view.as_view(), name = 'Ubicacion_view'),
    url(r'^reporte_apoyo/$', Reporte_Apoyo.as_view(), name = 'Reporte_Apoyo'),
    url(r'^consulta/$', consulta, name = 'consulta_view'),
     url(r'^ws/mensualdonacion/$',wsUltimoDonaciones,name='mensualdona_view'),
    url(r'^ws/mensualdefuncion/$',wsUltimoDefunciones,name='mensualdef_view'),
    url(r'^ws/mensualapoyo/$',wsUltimoApoyo,name='mensualap_view'),
    
    url(r'^reporte_mensual/$',ReporteMensual.as_view(),name='mensual_view'),
    url(r'^sephereventos/$',sephereventos.as_view(),name='sephereventos'),
    url(r'^eventos/$',wsEventos,name='eventos_view'),

    url(r'^Paciente_pdf/$',Pacientes_pdf.as_view(),name='pdfview'),
    url(r'^Apoyo_pdf/$',Apoyo_pdf.as_view(),name='pdfapoyview'),
    url(r'^Mensual_pdf/$',Mensual_pdf.as_view(),name='pdfmensualview'),
    url(r'^Defunciones_pdf/$',Defunciones_pdf.as_view(),name='pdfdefuview'),
    url(r'^Don_monetarias_pdf/$',Don_monetarias_pdf.as_view(),name='pdfdonmonuview'),
    url(r'^Don_especie_pdf/$',Don_especie_pdf.as_view(),name='pdfdonespuview'),
    url(r'^Personal_pdf/$',Personal_pdf.as_view(),name='pdfpersview'),
    url(r'^Detalle_Paciente_pdf/(?P<pk>\d+)$',Detalle_Paciente_pdf.as_view(),name='pdfpersview'),
    url(r'^Admin/$',Admin_view.as_view(),name='admin_view'),
]


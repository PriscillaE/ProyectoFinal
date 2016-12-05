from django.shortcuts import render
from django.views.generic import CreateView,TemplateView, UpdateView, View,FormView,ListView,DetailView, DeleteView
from .models import Donadores,Donaciones_Monetarias, Donaciones_Especie
from Pacientes.models import Seguimiento_Apoyo,Defunciones
from django.core.urlresolvers import reverse_lazy
from Pacientes.forms import HistorialMedico_Form
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum
from django.shortcuts import render_to_response
from datetime import datetime, time, date, timedelta
from django.http import HttpResponseRedirect,HttpResponse
from django.core import serializers

from django.contrib import auth
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime, time, date, timedelta

class Register_Donadores(CreateView):
	template_name ='registro_donadores.html'
	model = Donadores
	fields = '__all__'
	success_url = reverse_lazy('Register_Donadores')
class Register_Donaciones_Monetarias(CreateView):
	template_name ='registro_donadores_monetarias.html'
	model = Donaciones_Monetarias
	fields = '__all__'
	success_url = reverse_lazy('Donadores_monetarias_register_view')
class Register_Donaciones_Especie(CreateView):
	template_name ='registro_donadores_especie.html'
	model = Donaciones_Especie
	fields = '__all__'
	success_url = reverse_lazy('Donadores_especie_register_view')
class donadores_report(ListView):
	template_name = 'donadores_report.html'
	model = Donadores
class donaciones_monetarias_report(ListView):
	template_name = 'donaciones_monetarias_report.html'
	model = Donaciones_Monetarias
class donaciones_especie_report(ListView):
	template_name = 'donaciones_especie_report.html'
	model = Donaciones_Especie
class Editar_Donador(PermissionRequiredMixin,UpdateView):
	permission_required='Pacientes.editar'
  	model=Donadores
  	fields='__all__'
  	template_name='eliminar_donadores.html'
  	success_url=reverse_lazy('Donadores_eliminar_view')

class EditarDonaciones_monetarias(PermissionRequiredMixin, UpdateView):
	permission_required='Pacientes.editar'
  	model=Donaciones_Monetarias
  	fields='__all__'
  	template_name='eliminar_donaciones_monetarias.html'
  	success_url=reverse_lazy('Donaciones_monetarias_eliminar_view')

class Editar_Donaciones_especie(PermissionRequiredMixin, UpdateView):
	permission_required='Pacientes.editar'
  	model=Donaciones_Especie
  	fields='__all__'
  	template_name='eliminar_donaciones_especie.html'
  	success_url=reverse_lazy('Donadores_especie_eliminar_view')

def wsUltimoDonaciones(request):
	actual=datetime.now()
	data=serializers.serialize('json',Donaciones_Monetarias.objects.filter(Fecha__month=actual.month).select_related('Donador'))
	#print data
	return HttpResponse(data,content_type='application/json')

def wsUltimoDefunciones(request):
	actual=datetime.now()
	data=serializers.serialize('json',Defunciones.objects.filter(Fecha_apoyo__month=actual.month).select_related('Paciente'))
	#print data
	return HttpResponse(data,content_type='application/json')

def wsUltimoApoyo(request):
	actual=datetime.now()
	data=serializers.serialize('json',Seguimiento_Apoyo.objects.filter(Fecha_entrega__month=actual.month).select_related('Apoyo_Paciente'))
	#print data
	return HttpResponse(data,content_type='application/json')

class ReporteMensual(TemplateView):
	template_name='reporte_mensual.html'






class Mensual_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(200, 740, u"Reporte Mensual")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%Y'))

	def tabla1(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Donador', 'Cantidad', 'Forma pago')
		#Creamos una lista de tuplas que van a contener a las personas
		actual=datetime.now()
		detalles = [(p.Fecha, p.Donador.Donador_nombre, p.Cantidad, p.Forma_pago) for p in Donaciones_Monetarias.objects.filter(Fecha__month=actual.month).select_related('Donador')]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[130 , 130 , 130 , 130 ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				('TEXTCOLOR',(0,0),(3,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(3,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)    

	def tabla2(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Paciente', 'Cantidad', 'Nombre Recipiente')
		#Creamos una lista de tuplas que van a contener a las personas
		actual=datetime.now()
		detalles = [(p.Fecha_apoyo, p.Paciente.Paciente_nombre+" "+ p.Paciente.Paciente_apellido, p.Apoyo, p.Recipiente_nombre) for p in Defunciones.objects.filter(Fecha_apoyo__month=actual.month).select_related('Paciente')]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[130 , 130 , 130 , 130 ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				('TEXTCOLOR',(0,0),(3,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(3,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)           
	def tabla3(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha donacion','Paciente', 'Donacion monetaria', 'Donacion en especie')
		#Creamos una lista de tuplas que van a contener a las persona
		actual=datetime.now()
		detalles = [(p.Fecha_entrega,p.Apoyo_Paciente.Paciente_nombre+" "+ p.Apoyo_Paciente.Paciente_apellido, p.Donacion_monetaria, p.Donacion_especie) for p in Seguimiento_Apoyo.objects.filter(Fecha_entrega__month=actual.month,Donacion_especie=" ").select_related('Apoyo_Paciente')]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[ 130, 130 , 130 , 130])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				('TEXTCOLOR',(0,0),(3,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(3,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)    

	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 650
		self.tabla1(pdf, y)
		y = 400
		self.tabla2(pdf, y)
		y = 200
		self.tabla3(pdf, y) 
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response

class Don_monetarias_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(120, 740, u"Reporte Donaciones monetarias")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%d/%Y'))

	def tabla1(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Donador', 'Cantidad', 'Forma pago')
		#Creamos una lista de tuplas que van a contener a las personas
		actual=datetime.now()
		detalles = [(p.Fecha, p.Donador.Donador_nombre, p.Cantidad, p.Forma_pago) for p in Donaciones_Monetarias.objects.all().select_related('Donador')]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[130 , 130 , 130 , 130 ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				('TEXTCOLOR',(0,0),(3,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(3,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)    

	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 650
		self.tabla1(pdf, y)
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response

class Don_especie_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(120, 740, u"Reporte Donaciones en especie")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%d/%Y'))

	def tabla1(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Donador', 'Descripcion', 'Unidades','Cantidad')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.Fecha, p.Donador.Donador_nombre, p.Descripcion, p.Cantidad, p.Cantidad) for p in Donaciones_Especie.objects.all().select_related('Donador')]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[100 , 100, 100 , 100 ,90])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(4,0),'CENTER'),
				('TEXTCOLOR',(0,0),(4,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(4,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)    

	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 650
		self.tabla1(pdf, y)
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response
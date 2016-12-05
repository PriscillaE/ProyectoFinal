from django.shortcuts import render
from django.views.generic import CreateView,TemplateView, UpdateView, FormView,ListView,DetailView,View, DeleteView
from Pacientes.models import Seguimiento_Apoyo,Paciente,Historial_Medico,Defunciones
from django.core.urlresolvers import reverse_lazy
from Pacientes.forms import HistorialMedico_Form
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import Consulta_form

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

class Registro_paciente(CreateView):
	template_name='registro_paciente.html'
	model=Paciente
	fields='__all__'
	success_url=reverse_lazy('reporte_pacientes')

class Reporte_Paciente(ListView):
	template_name='reporte_pacientes.html'
	model=Paciente

# class Eliminar_Paciente(DeleteView):
#     model = Paciente
#     success_url = reverse_lazy('reporte_pacientes')

class EditarPaciente(PermissionRequiredMixin,UpdateView):
	permission_required='Pacientes.editar'
	model=Paciente
  	fields='__all__'
  	template_name='editar_paciente.html'
  	success_url=reverse_lazy('reporte_pacientes')

def Paciente_detalle(request,pk):
	p=Paciente.objects.get(id=pk)
	ph=Historial_Medico.objects.filter(Paciente_hm=pk)
	pa=Seguimiento_Apoyo.objects.filter(Apoyo_Paciente=pk)
	return render(request,'detalle_paciente.html',{'list':p,'list1':ph,'list2':pa}) 	
 	

class Registro_Historial(CreateView):
	template_name='registro_medico.html'
	model=Historial_Medico
	fields='__all__'
	success_url=reverse_lazy('reporte_pacientes')

#def Registro_Medico(request,pk):
	# form=HistorialMedico_Form(request.POST or None)
	# if request.method=='POST':
	# 	if form.is_valid():
	# 		p_paciente=pk
	# 		p_fecha=form.cleaned_data['Fecha']
	# 		p_diagnostico = form.cleaned_data['Diagnostico']

	# 		hm=Historial_Medico.objects.create(Paciente_hm=p_paciente,Fecha=p_fecha,Diagnostico=p_diagnostico)

	# 		return HttpResponseRedirect('/')
	# else:
	# 	form=HistorialMedico_Form()
	# ctx={'form':form}
	# return render(request,'registro_medico.html',ctx)

class Registro_Apoyo(CreateView):
	template_name='registro_apoyo.html'
	model=Seguimiento_Apoyo
	fields='__all__'
	success_url=reverse_lazy('Reporte_Apoyo')

class Reporte_Apoyo(ListView):
	template_name='reporte_apoyo.html'
	model=Seguimiento_Apoyo


class Registro_Defunciones(CreateView):
	template_name='registro_defunciones.html'
	model=Defunciones
	fields='__all__'
	success_url=reverse_lazy('ReporteDef_view')

class Reporte_Defunciones(ListView):
	template_name='reporte_defunciones.html'
	model=Defunciones

# class Eliminar_Defunciones(DeleteView):
#     model = Defunciones
#     success_url = reverse_lazy('reporte_defunciones')
def consulta (request):
	b = Paciente.objects.filter(Estado_salud='RE')
	c = Paciente.objects.filter(Estado_salud='TR')
	d = Paciente.objects.filter(Estado_salud='DEP')
	form = Consulta_form(request.POST or None)
	return render (request, 'consulta.html', {'list1' :b, 'list2' :c, 'list3' :d})



class Pacientes_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(200, 740, u"Reporte Pacientes")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%d/%Y'))

	def tabla(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Nombre', 'Apellido', 'Diagnostico', 'Clinica','Tutor','Estado Salud')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.Paciente_nombre, p.Paciente_apellido, p.Paciente_diagnostico, p.Paciente_clinica,p.Tutor_Padre,p.Estado_salud) for p in Paciente.objects.all()]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[95 , 95 , 95 , 95,95,95 ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(5,0),'CENTER'),
				('TEXTCOLOR',(0,0),(5,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(5,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 12,y)                
           

	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 620
		self.tabla(pdf, y)
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response


class Apoyo_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(180, 740, u"Reporte Pacientes-Donaciones")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%d/%Y'))

	def tabla(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Paciente', 'Apoyo monetario', 'Apoyo en especie', 'Fecha de apoyo')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.Apoyo_Paciente.Paciente_nombre + " "+ p.Apoyo_Paciente.Paciente_apellido, p.Donacion_monetaria, p.Donacion_especie, p.Fecha_entrega) for p in Seguimiento_Apoyo.objects.select_related("Apoyo_Paciente").all()]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[120 , 120 , 120 , 120 ])
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
		detalle_orden.drawOn(pdf, 60,y)                
           

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
		self.tabla(pdf, y)

		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response

class Defunciones_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(200, 740, u"Reportes Apoyos Defunciones")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%d/%Y'))  

	def tabla1(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Paciente', 'Cantidad', 'Nombre Recipiente')
		#Creamos una lista de tuplas que van a contener a las personas
		actual=datetime.now()
		detalles = [(p.Fecha_apoyo, p.Paciente.Paciente_nombre+" "+ p.Paciente.Paciente_apellido, p.Apoyo, p.Recipiente_nombre) for p in Defunciones.objects.all().select_related('Paciente')]

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

class Detalle_Paciente_pdf(View):
	def cabecera(self,pdf,pk):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(200, 740, u"Reporte Paciente")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%Y')) 
		p=Paciente.objects.get(pk=pk) 
		pdf.setFont("Helvetica", 12)
		pdf.drawString(200, 690, p.Paciente_nombre + " " + p.Paciente_apellido)
		pdf.drawString(200, 674, p.Paciente_diagnostico + "    "+p.Paciente_clinica)
		pdf.drawString(200, 660, p.Estado_salud )
	def tabla1(self,pdf,y,pk):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Diagnostico')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.Fecha, p.Diagnostico) for p in Historial_Medico.objects.filter(Paciente_hm=pk).select_related()]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[130 , 200  ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(1,0),'CENTER'),
				('TEXTCOLOR',(0,0),(1,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(1,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 100,y)           
	
	def tabla2(self,pdf,y,pk):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha donacion', 'Donacion monetaria','Donacion en especie')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(p.Fecha_entrega, p.Donacion_monetaria,p.Donacion_especie) for p in Seguimiento_Apoyo.objects.filter(Apoyo_Paciente=pk).select_related()]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[130 , 200,200  ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(2,0),'CENTER'),
				('TEXTCOLOR',(0,0),(2,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(2,0),colors.gainsboro),
				
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
		idpk=kwargs['pk']
		self.cabecera(pdf,idpk)
		y = 550
		self.tabla1(pdf, y,idpk)
		y = 300
		self.tabla2(pdf, y,idpk)
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response
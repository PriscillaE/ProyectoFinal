from django.shortcuts import render
from django.views.generic import CreateView,TemplateView, UpdateView, FormView,ListView,DetailView, DeleteView
from .models import Paciente,Historial_Medico,Donadores,Donaciones_Monetarias, Donaciones_Especie
from .models import Seguimiento_Apoyo,Minutas,Personal,Eventos,Defunciones,Administradores
from django.core.urlresolvers import reverse_lazy
from .forms import HistorialMedico_Form
from django.template import RequestContext
from django.contrib.auth.mixins import PermissionRequiredMixin


class Index_view(TemplateView):
	template_name='index.html'
	


class Mision_view(TemplateView):
	template_name = 'mision.html'

class Historia_view(TemplateView):
	template_name = 'historia.html'

class Ubicacion_view(TemplateView):
	template_name = 'ubicacion.html'

class Registro_paciente(CreateView):
	template_name='registro_paciente.html'
	model=Paciente
	fields='__all__'
	success_url=reverse_lazy('reporte_pacientes')

class Reporte_Paciente(ListView):
	template_name='reporte_pacientes.html'
	model=Paciente

class Eliminar_Paciente(DeleteView):
   model = Paciente
   success_url = reverse_lazy('reporte_pacientes')

class EditarPaciente(PermissionRequiredMixin, UpdateView):
	permission_required='home.editar'
  	model=Paciente
  	fields='__all__'
  	template_name='editar_paciente.html'
  	success_url=reverse_lazy('reporte_pacientes')

def Paciente_detalle(request,pk):
	p=Paciente.objects.get(id=pk)
	ph=Historial_Medico.objects.filter(Paciente_hm=pk)
	return render(request,'detalle_paciente.html',{'list':p,'list1':ph}) 	
 	

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

class Registro_Minutas(CreateView):
	template_name='registro_minutas.html'
	model=Minutas
	fields='__all__'
	success_url=reverse_lazy('reporte_minutas')

class Detalle_minuta(DetailView):
	template_name='detalle_minuta.html'
	model=Minutas

class Reporte_Minutas(ListView):
	template_name='reporte_minutas.html'
	model=Minutas

class Registro_Apoyo(CreateView):
	template_name='registro_apoyo.html'
	model=Seguimiento_Apoyo
	fields='__all__'
	success_url=reverse_lazy('reporte_apoyo')

class Reporte_Apoyo(ListView):
	template_name='reporte_apoyo.html'
	model=Seguimiento_Apoyo


class Registro_Defunciones(CreateView):
	template_name='registro_defunciones.html'
	model=Defunciones
	fields='__all__'
	success_url=reverse_lazy('reporte_defunciones')

class Reporte_Defunciones(ListView):
	template_name='reporte_defunciones.html'
	model=Defunciones

class Eliminar_Defunciones(DeleteView):
    model = Defunciones
    success_url = reverse_lazy('reporte_defunciones')

class Registro_Eventos(CreateView):
	template_name='registro_eventos.html'
	model=Eventos
	fields='__all__'
	success_url=reverse_lazy('reporte_eventos')

class Eliminar_Eventos(DeleteView):
    model = Eventos
    success_url = reverse_lazy('reporte_eventos')

class Editar_Evento(UpdateView):
  	model=Eventos
  	fields='__all__'
  	template_name='editar_evento.html'
  	success_url=reverse_lazy('reporte_eventos')

class Reporte_Eventos(ListView):
	template_name='reporte_eventos.html'
	model=Eventos

class Detalle_eventos(DetailView):
	template_name='detalle_evento.html'
	model=Eventos

class Registro_Personal(CreateView):
	template_name='registro_personal.html'
	model=Personal
	fields='__all__'
	success_url=reverse_lazy('reporte_personal')

class Eliminar_Personal(DeleteView):
    model = Personal
    success_url = reverse_lazy('reporte_personal')

class Editar_Personal(UpdateView):
  	model=Personal
  	fields='__all__'
  	template_name='editar_personal.html'
  	success_url=reverse_lazy('reporte_personal')

class Reporte_Personal(ListView):
	template_name='reporte_personal.html'
	model=Personal

# @login_required
# def validate_password(request):
#     form = ValidatePasswordForm(request.POST or None, user=request.user)
#     if request.method == 'POST':
#         if form.is_valid():
#             # do something upon validation
#             # disable account
#             pass
#     request_dict = {'form': form}
#     return render_to_response('editar_paciente.html',
#         request_dict, context_instance=RequestContext(request))
#modal, para contrasena para eliminar y editar
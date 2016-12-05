from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente,Historial_Medico,Defunciones,Seguimiento_Apoyo

from datetime import datetime, time, date, timedelta

class Pacientes_Form(forms.ModelForm):
	class Meta:
		model=Paciente
		fields='__all__'
	def clean(self):
		fecha_nacimiento=self.cleaned_data["Paciente_fnacimiento"]
		nino=abs(date.today()-fecha_nacimiento)
		if ((nino.days/365.0)>=18):
			raise forms.ValidationError("Edad incorrecta")
		return cleaned_data

class HistorialMedico_Form(forms.ModelForm):
	class Meta:
		model=Historial_Medico
		fields='__all__'



class Apoyo_Form(forms.ModelForm):
	class Meta:
		model=Seguimiento_Apoyo
		fields='__all__'

class Defunciones_Form(forms.ModelForm):
	class Meta:
		model=Defunciones
		fields='__all__'
class Consulta_form(forms.ModelForm):
	class Meta:
		model = Paciente
		fields = '__all__'
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Minutas,Personal,Eventos,Administradores
from datetime import datetime, time, date, timedelta



class Minutas_Form(forms.ModelForm):
	class Meta:
		model=Minutas
		fields='__all__'

class Personal_Form(forms.ModelForm):
	class Meta:
		model=Personal
		fields='__all__'

class Eventos_Form(forms.ModelForm):
	class Meta:
		model=Eventos
		fields='__all__'



class Adminsitradores_Form(UserCreationForm):
	Admon_nombre=forms.CharField(max_length=40)
	Admon_tel=forms.CharField(max_length=15)
	Admon_correo=forms.EmailField()

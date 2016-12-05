from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Donadores,Donaciones_Monetarias, Donaciones_Especie
from datetime import datetime, time, date, timedelta

class Donadores_Form(forms.ModelForm):
	class Meta:
		model=Donadores
		fields='__all__'

class DonacionesMonetarias_Form(forms.ModelForm):
	class Meta:
		model=Donaciones_Monetarias
		fields='__all__'

class DonadoresEspecia_Form(forms.ModelForm):
	class Meta:
		model=Donaciones_Especie
		fields='__all__'
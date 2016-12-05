from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente,Historial_Medico,Donadores,Donaciones_Monetarias, Donaciones_Especie
from .models import Seguimiento_Apoyo,Minutas,Personal,Eventos,Defunciones,Administradores
from datetime import datetime, time, date, timedelta
#from django.contrib.auth.models import check_password

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

class Apoyo_Form(forms.ModelForm):
	class Meta:
		model=Seguimiento_Apoyo
		fields='__all__'

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

class Defunciones_Form(forms.ModelForm):
	class Meta:
		model=Defunciones
		fields='__all__'

class Adminsitradores_Form(UserCreationForm):
	Admon_nombre=forms.CharField(max_length=40)
	Admon_tel=forms.CharField(max_length=15)
	Admon_correo=forms.EmailField()

# class ValidatePasswordForm(forms.Form):
#     password = forms.CharField(label="Your Password",
#         widget=forms.PasswordInput)

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(ValidatePasswordForm, self).__init__(*args, **kwargs)

#     def clean_password(self):
#         password = self.cleaned_data['password']
#         valid = check_password(password, self.user.password)
#         if not valid:
#             raise forms.ValidationError('Invalid password')
#         return password
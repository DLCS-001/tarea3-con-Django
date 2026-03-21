from django import forms
from .models import Catedratico

class CatedraticoForm(forms.ModelForm):
    class Meta:
        model = Catedratico
        fields = ['codigo', 'nombre', 'apellido', 'email', 'telefono', 'especialidad', 'is_active']
        
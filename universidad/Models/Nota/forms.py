from django import forms
from .models import Nota
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['alumno', 'curso', 'nota1', 'nota2', 'nota3', 'examen_final']
        widgets = {
            'alumno': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'nota1': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0 - 100'
            }),
            'nota2': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0 - 100'
            }),
            'nota3': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0 - 100'
            }),
            'examen_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0 - 100'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        nota1 = cleaned_data.get('nota1')
        nota2 = cleaned_data.get('nota2')
        nota3 = cleaned_data.get('nota3')

        # Validar que al menos una nota esté ingresada
        if nota1 is None and nota2 is None and nota3 is None:
            raise forms.ValidationError("Debe ingresar al menos una calificación parcial.")

        return cleaned_data
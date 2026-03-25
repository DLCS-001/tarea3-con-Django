from django import forms
from .models import Nota

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
                'max': str(Nota.PARCIAL_1_MAXIMO),
                'placeholder': f'0 - {Nota.PARCIAL_1_MAXIMO}'
            }),
            'nota2': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': str(Nota.PARCIAL_2_MAXIMO),
                'placeholder': f'0 - {Nota.PARCIAL_2_MAXIMO}'
            }),
            'nota3': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': str(Nota.ZONA_MAXIMA),
                'placeholder': f'0 - {Nota.ZONA_MAXIMA}'
            }),
            'examen_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': str(Nota.EXAMEN_FINAL_MAXIMO),
                'placeholder': f'0 - {Nota.EXAMEN_FINAL_MAXIMO}'
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

        limites = {
            'nota1': Nota.PARCIAL_1_MAXIMO,
            'nota2': Nota.PARCIAL_2_MAXIMO,
            'nota3': Nota.ZONA_MAXIMA,
            'examen_final': Nota.EXAMEN_FINAL_MAXIMO,
        }
        for field_name, limite in limites.items():
            value = cleaned_data.get(field_name)
            if value is not None and not 0 <= value <= limite:
                self.add_error(field_name, f"La calificación debe estar entre 0 y {limite}.")

        return cleaned_data

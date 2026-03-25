from django import forms
from .models import InscripcionAlumno
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso
import datetime


class InscripcionAlumnoForm(forms.ModelForm):
    class Meta:
        model = InscripcionAlumno
        fields = ['alumno', 'curso', 'anio', 'semestre', 'estado']
        widgets = {
            'alumno': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2000',
                'max': datetime.datetime.now().year + 5,
                'value': datetime.datetime.now().year
            }),
            'semestre': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '2',
                'placeholder': '1 o 2'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_semestre(self):
        semestre = self.cleaned_data.get('semestre')
        if semestre not in [1, 2]:
            raise forms.ValidationError("El semestre debe ser 1 o 2.")
        return semestre

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get('alumno')
        curso = cleaned_data.get('curso')
        anio = cleaned_data.get('anio')
        semestre = cleaned_data.get('semestre')

        if alumno and curso and anio and semestre:
            # Verificar si ya existe una inscripción para este alumno en el mismo período
            if InscripcionAlumno.objects.filter(
                    alumno=alumno,
                    curso=curso,
                    anio=anio,
                    semestre=semestre
            ).exists():
                raise forms.ValidationError(
                    f"El alumno {alumno} ya está inscrito en el curso {curso} "
                    f"para el {semestre}° semestre de {anio}."
                )

        return cleaned_data
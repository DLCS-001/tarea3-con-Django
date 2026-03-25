from django import forms
from .models import AsignacionCurso
import datetime


class AsignacionCursoForm(forms.ModelForm):
    class Meta:
        model = AsignacionCurso
        fields = ['curso', 'catedratico', 'anio', 'semestre', 'seccion']
        widgets = {
            'curso': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'catedratico': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2000',
                'max': datetime.datetime.now().year + 5,
                'value': datetime.datetime.now().year
            }),
            'semestre': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'seccion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '1',
                'placeholder': 'A, B, C, etc.'
            }),
        }

    def clean_seccion(self):
        seccion = self.cleaned_data.get('seccion')
        if seccion:
            seccion = seccion.upper()
            if len(seccion) != 1 or not seccion.isalpha():
                raise forms.ValidationError("La sección debe ser una sola letra (A, B, C, etc.)")
        return seccion

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')
        anio = cleaned_data.get('anio')
        semestre = cleaned_data.get('semestre')
        seccion = cleaned_data.get('seccion')

        if curso and anio and semestre and seccion:
            # Verificar si ya existe una asignación para este curso en el mismo período
            existing = AsignacionCurso.objects.filter(
                curso=curso,
                anio=anio,
                semestre=semestre,
                seccion=seccion,
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(
                    f"Ya existe una asignación para el curso {curso.nombre} "
                    f"en el {semestre}° semestre de {anio}, sección {seccion}."
                )

        return cleaned_data

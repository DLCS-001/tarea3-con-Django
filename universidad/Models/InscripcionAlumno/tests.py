from django.test import TestCase

from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso

from .forms import InscripcionAlumnoForm
from .models import InscripcionAlumno


class InscripcionAlumnoFormTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(
            carnet='A100',
            first_name='Ana',
            last_name='Ramirez',
            email='ana@example.com',
            gender='F',
            birth_date='2002-03-03',
        )
        self.curso = Curso.objects.create(
            codigo='MAT101',
            nombre='Matematica',
            creditos=4,
        )
        self.inscripcion = InscripcionAlumno.objects.create(
            alumno=self.alumno,
            curso=self.curso,
            anio=2026,
            semestre=1,
            estado='activo',
        )

    def test_editing_same_instance_is_valid(self):
        form = InscripcionAlumnoForm(
            data={
                'alumno': self.alumno.pk,
                'curso': self.curso.pk,
                'anio': 2026,
                'semestre': 1,
                'estado': 'activo',
            },
            instance=self.inscripcion,
        )

        self.assertTrue(form.is_valid(), form.errors)

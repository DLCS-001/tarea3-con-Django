from django.test import TestCase

from universidad.Models.Catedratico.models import Catedratico
from universidad.Models.Curso.models import Curso

from .forms import AsignacionCursoForm
from .models import AsignacionCurso


class AsignacionCursoFormTests(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo='FIS101',
            nombre='Fisica',
            creditos=5,
        )
        self.catedratico = Catedratico.objects.create(
            codigo='CAT01',
            nombre='Luis',
            apellido='Mendez',
            email='luis@example.com',
        )
        self.asignacion = AsignacionCurso.objects.create(
            curso=self.curso,
            catedratico=self.catedratico,
            anio=2026,
            semestre=1,
            seccion='A',
        )

    def test_editing_same_instance_is_valid(self):
        form = AsignacionCursoForm(
            data={
                'curso': self.curso.pk,
                'catedratico': self.catedratico.pk,
                'anio': 2026,
                'semestre': 1,
                'seccion': 'A',
            },
            instance=self.asignacion,
        )

        self.assertTrue(form.is_valid(), form.errors)

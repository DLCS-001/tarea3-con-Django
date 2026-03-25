from django.test import TestCase

from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso

from .forms import NotaForm
from .models import Nota


class NotaTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(
            carnet='A200',
            first_name='Jose',
            last_name='Castillo',
            email='jose@example.com',
            gender='M',
            birth_date='2001-04-04',
        )
        self.curso = Curso.objects.create(
            codigo='QUI101',
            nombre='Quimica',
            creditos=4,
        )

    def test_save_calculates_total_zone_and_final_over_100_points(self):
        nota = Nota.objects.create(
            alumno=self.alumno,
            curso=self.curso,
            nota1=15,
            nota2=15,
            nota3=35,
            examen_final=35,
        )

        self.assertEqual(nota.zona, 65)
        self.assertEqual(nota.nota_final, 100)

    def test_save_resets_calculated_fields_when_scores_are_removed(self):
        nota = Nota.objects.create(
            alumno=self.alumno,
            curso=self.curso,
            nota1=15,
            nota2=15,
            nota3=35,
            examen_final=35,
        )

        nota.nota1 = None
        nota.nota2 = None
        nota.nota3 = None
        nota.examen_final = None
        nota.save()
        nota.refresh_from_db()

        self.assertIsNone(nota.zona)
        self.assertIsNone(nota.nota_final)

    def test_form_rejects_out_of_range_scores(self):
        form = NotaForm(
            data={
                'alumno': self.alumno.pk,
                'curso': self.curso.pk,
                'nota1': 16,
                'nota2': '',
                'nota3': 36,
                'examen_final': 40,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('nota1', form.errors)
        self.assertIn('nota3', form.errors)
        self.assertIn('examen_final', form.errors)

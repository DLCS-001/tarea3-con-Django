from django.test import TestCase
from django.urls import reverse

from .models import Alumno


class AlumnoViewsTests(TestCase):
    def test_list_can_filter_by_carnet(self):
        alumno = Alumno.objects.create(
            carnet='A001',
            first_name='Juan',
            last_name='Perez',
            email='juan@example.com',
            gender='M',
            birth_date='2000-01-01',
        )
        Alumno.objects.create(
            carnet='A002',
            first_name='Maria',
            last_name='Lopez',
            email='maria@example.com',
            gender='F',
            birth_date='2001-02-02',
        )

        response = self.client.get(reverse('alumno:list'), {'q': 'A001'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, alumno.carnet)
        self.assertNotContains(response, 'A002')

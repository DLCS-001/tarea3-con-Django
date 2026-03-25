from django.db import models

class Alumno(models.Model):
    carnet = models.CharField(max_length=20, unique=True, verbose_name="Carnet")  # NUEVO
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], verbose_name="Género")
    birth_date = models.DateField(verbose_name="Fecha de nacimiento")
    enrolled_at = models.DateField(auto_now_add=True, verbose_name="Fecha de inscripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.carnet} - {self.first_name} {self.last_name}"

    class Meta:
        db_table = 'alumno'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['carnet']
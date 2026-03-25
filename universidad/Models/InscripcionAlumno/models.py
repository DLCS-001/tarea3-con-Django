from django.db import models
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso


class InscripcionAlumno(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('retirado', 'Retirado'),
        ('aprobado', 'Aprobado'),
        ('reprobado', 'Reprobado'),
    ]

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='inscripciones',
        verbose_name="Alumno"
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='inscripciones',
        verbose_name="Curso"
    )
    anio = models.IntegerField(
        verbose_name="Año",
        help_text="Año académico (ej: 2024)"
    )
    semestre = models.IntegerField(
        verbose_name="Semestre",
        help_text="1 = Primer Semestre, 2 = Segundo Semestre"
    )
    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de inscripción"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name="Estado"
    )

    def __str__(self):
        return f"{self.alumno} - {self.curso} ({self.anio} - {self.semestre}° Sem)"

    class Meta:
        db_table = 'inscripcion_alumno'
        verbose_name = 'Inscripción de Alumno'
        verbose_name_plural = 'Inscripciones de Alumnos'
        unique_together = ['alumno', 'curso', 'anio', 'semestre']
        ordering = ['-fecha_inscripcion']
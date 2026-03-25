from django.db import models
from universidad.Models.Curso.models import Curso
from universidad.Models.Catedratico.models import Catedratico


class AsignacionCurso(models.Model):
    SEMESTRE_CHOICES = [
        (1, 'Primer Semestre'),
        (2, 'Segundo Semestre'),
    ]

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name="Curso"
    )
    catedratico = models.ForeignKey(
        Catedratico,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name="Catedrático"
    )
    anio = models.IntegerField(
        verbose_name="Año",
        help_text="Año académico (ej: 2024)"
    )
    semestre = models.IntegerField(
        choices=SEMESTRE_CHOICES,
        verbose_name="Semestre",
        help_text="1 = Primer Semestre, 2 = Segundo Semestre"
    )
    seccion = models.CharField(
        max_length=1,
        verbose_name="Sección",
        help_text="Letra de la sección (A, B, C, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de asignación")

    def __str__(self):
        return f"{self.curso} - {self.catedratico} ({self.anio} - {self.semestre}° Sem - Secc {self.seccion})"

    class Meta:
        db_table = 'asignacion_curso'
        verbose_name = 'Asignación de Curso'
        verbose_name_plural = 'Asignaciones de Cursos'
        unique_together = ['curso', 'anio', 'semestre', 'seccion']
        ordering = ['-anio', '-semestre', 'curso__nombre']
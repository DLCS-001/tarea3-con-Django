from django.db import models
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso


class Nota(models.Model):
    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name="Alumno"
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name="Curso"
    )
    nota1 = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Nota 1",
        help_text="Primera evaluación (0-100)"
    )
    nota2 = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Nota 2",
        help_text="Segunda evaluación (0-100)"
    )
    nota3 = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Nota 3",
        help_text="Tercera evaluación (0-100)"
    )
    zona = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Zona",
        help_text="Promedio de notas (calculado automáticamente)"
    )
    examen_final = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Examen Final",
        help_text="Nota del examen final (0-100)"
    )
    nota_final = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Nota Final",
        help_text="Nota final del curso (calculada automáticamente)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def save(self, *args, **kwargs):
        # Calcular zona como promedio de las 3 notas
        notas = [self.nota1, self.nota2, self.nota3]
        notas_validas = [n for n in notas if n is not None]
        if notas_validas:
            self.zona = round(sum(notas_validas) / len(notas_validas), 2)

        # Calcular nota final si zona y examen final existen
        if self.zona is not None and self.examen_final is not None:
            self.nota_final = round((self.zona + self.examen_final) / 2, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno} - {self.curso}"

    class Meta:
        db_table = 'nota'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        unique_together = ['alumno', 'curso']
        ordering = ['-created_at']
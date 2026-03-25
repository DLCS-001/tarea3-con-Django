from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso


class Nota(models.Model):
    PARCIAL_1_MAXIMO = 15
    PARCIAL_2_MAXIMO = 15
    ZONA_MAXIMA = 35
    EXAMEN_FINAL_MAXIMO = 35

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
        validators=[MinValueValidator(0), MaxValueValidator(PARCIAL_1_MAXIMO)],
        verbose_name="Parcial 1",
        help_text="Primera evaluación (0-15)"
    )
    nota2 = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(PARCIAL_2_MAXIMO)],
        verbose_name="Parcial 2",
        help_text="Segunda evaluación (0-15)"
    )
    nota3 = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(ZONA_MAXIMA)],
        verbose_name="Zona de tareas",
        help_text="Zona acumulada de tareas (0-35)"
    )
    zona = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Total zona",
        help_text="Suma de Parcial 1, Parcial 2 y Zona de tareas"
    )
    examen_final = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(EXAMEN_FINAL_MAXIMO)],
        verbose_name="Examen Final",
        help_text="Nota del examen final (0-35)"
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
        # La zona es la suma de parciales y tareas; la nota final suma zona y examen.
        componentes_zona = [self.nota1, self.nota2, self.nota3]
        zona_componentes_validos = [n for n in componentes_zona if n is not None]
        if zona_componentes_validos:
            self.zona = round(sum(zona_componentes_validos), 2)
        else:
            self.zona = None

        nota_final_componentes = zona_componentes_validos.copy()
        if self.examen_final is not None:
            nota_final_componentes.append(self.examen_final)

        if nota_final_componentes:
            self.nota_final = round(sum(nota_final_componentes), 2)
        else:
            self.nota_final = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno} - {self.curso}"

    class Meta:
        db_table = 'nota'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        unique_together = ['alumno', 'curso']
        ordering = ['-created_at']

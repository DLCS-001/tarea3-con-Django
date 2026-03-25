import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nota', '0003_add_grade_validators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='examen_final',
            field=models.FloatField(blank=True, help_text='Nota del examen final (0-35)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(35)], verbose_name='Examen Final'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota1',
            field=models.FloatField(blank=True, help_text='Primera evaluación (0-15)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)], verbose_name='Parcial 1'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota2',
            field=models.FloatField(blank=True, help_text='Segunda evaluación (0-15)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)], verbose_name='Parcial 2'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota3',
            field=models.FloatField(blank=True, help_text='Zona acumulada de tareas (0-35)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(35)], verbose_name='Zona de tareas'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='zona',
            field=models.FloatField(blank=True, help_text='Suma de Parcial 1, Parcial 2 y Zona de tareas', null=True, verbose_name='Total zona'),
        ),
    ]

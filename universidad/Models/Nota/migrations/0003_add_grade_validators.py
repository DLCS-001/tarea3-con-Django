import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nota', '0002_alter_nota_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='examen_final',
            field=models.FloatField(blank=True, help_text='Nota del examen final (0-100)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Examen Final'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota1',
            field=models.FloatField(blank=True, help_text='Primera evaluación (0-100)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Nota 1'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota2',
            field=models.FloatField(blank=True, help_text='Segunda evaluación (0-100)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Nota 2'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='nota3',
            field=models.FloatField(blank=True, help_text='Tercera evaluación (0-100)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Nota 3'),
        ),
    ]

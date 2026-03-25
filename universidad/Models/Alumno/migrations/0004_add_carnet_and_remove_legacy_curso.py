from django.db import migrations, models


def populate_carnet(apps, schema_editor):
    Alumno = apps.get_model('Alumno', 'Alumno')
    for alumno in Alumno.objects.filter(carnet__isnull=True).order_by('pk'):
        alumno.carnet = f"A{alumno.pk:06d}"
        alumno.save(update_fields=['carnet'])


class Migration(migrations.Migration):

    dependencies = [
        ('Alumno', '0003_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='carnet',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.RunPython(populate_carnet, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='alumno',
            name='carnet',
            field=models.CharField(max_length=20, unique=True, verbose_name='Carnet'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='birth_date',
            field=models.DateField(verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='enrolled_at',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha de inscripción'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='gender',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Género'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Teléfono'),
        ),
        migrations.AlterModelOptions(
            name='alumno',
            options={'ordering': ['carnet'], 'verbose_name': 'Alumno', 'verbose_name_plural': 'Alumnos'},
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
    ]

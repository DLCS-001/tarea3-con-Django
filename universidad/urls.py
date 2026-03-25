from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('alumnos/', include('universidad.Models.Alumno.urls')),
    path('cursos/', include('universidad.Models.Curso.urls')),
    path('catedraticos/', include('universidad.Models.Catedratico.urls')),
    path('notas/', include('universidad.Models.Nota.urls')),
    path('asignaciones/', include('universidad.Models.AsignacionCurso.urls')),
    path('inscripciones/', include('universidad.Models.InscripcionAlumno.urls')),
]

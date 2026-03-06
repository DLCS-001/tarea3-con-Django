from django.shortcuts import render

from django.shortcuts import render
from universidad.Models.Alumno.models import Alumno
def dashboard(request):
    context = {
        'total_alumnos'   : Alumno.objects.count(),
        'activos'         : Alumno.objects.filter(is_active=True).count(),
        'inactivos'       : Alumno.objects.filter(is_active=False).count(),
    }
    return render(request, 'core/dashboard.html', context)

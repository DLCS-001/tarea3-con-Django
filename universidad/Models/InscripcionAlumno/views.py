from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import InscripcionAlumno
from .forms import InscripcionAlumnoForm


def inscripcion_list(request):
    """Listado de todas las inscripciones"""
    query = request.GET.get('q', '')
    inscripciones = InscripcionAlumno.objects.select_related('alumno', 'curso').all()

    if query:
        inscripciones = inscripciones.filter(
            models.Q(alumno__first_name__icontains=query) |
            models.Q(alumno__last_name__icontains=query) |
            models.Q(alumno__carnet__icontains=query) |
            models.Q(curso__nombre__icontains=query) |
            models.Q(curso__codigo__icontains=query) |
            models.Q(estado__icontains=query)
        )

    return render(request, 'inscripcion_alumno/list.html', {
        'inscripciones': inscripciones,
        'query': query,
        'total_inscripciones': inscripciones.count()
    })


def inscripcion_create(request):
    """Crear una nueva inscripción"""
    if request.method == 'POST':
        form = InscripcionAlumnoForm(request.POST)
        if form.is_valid():
            inscripcion = form.save()
            messages.success(
                request,
                f'Inscripción registrada: {inscripcion.alumno} se inscribió en {inscripcion.curso} '
                f'({inscripcion.anio} - {inscripcion.semestre}° Semestre)'
            )
            return redirect('inscripcionalumno:list')
    else:
        form = InscripcionAlumnoForm()

    return render(request, 'inscripcion_alumno/form.html', {
        'form': form,
        'title': 'Nueva Inscripción de Alumno',
        'button_text': 'Registrar Inscripción'
    })


def inscripcion_edit(request, pk):
    """Editar una inscripción existente"""
    inscripcion = get_object_or_404(InscripcionAlumno, pk=pk)

    if request.method == 'POST':
        form = InscripcionAlumnoForm(request.POST, instance=inscripcion)
        if form.is_valid():
            inscripcion = form.save()
            messages.success(
                request,
                f'Inscripción actualizada: {inscripcion.alumno} - {inscripcion.curso} '
                f'({inscripcion.anio} - {inscripcion.semestre}° Semestre) - Estado: {inscripcion.get_estado_display()}'
            )
            return redirect('inscripcionalumno:list')
    else:
        form = InscripcionAlumnoForm(instance=inscripcion)

    return render(request, 'inscripcion_alumno/form.html', {
        'form': form,
        'title': f'Editar Inscripción: {inscripcion.alumno} - {inscripcion.curso}',
        'button_text': 'Actualizar Inscripción',
        'inscripcion': inscripcion
    })


def inscripcion_delete(request, pk):
    """Eliminar una inscripción"""
    inscripcion = get_object_or_404(InscripcionAlumno, pk=pk)

    if request.method == 'POST':
        alumno_nombre = str(inscripcion.alumno)
        curso_nombre = str(inscripcion.curso)
        inscripcion.delete()
        messages.success(
            request,
            f'Inscripción eliminada: {alumno_nombre} ya no está inscrito en {curso_nombre} '
            f'({inscripcion.anio} - {inscripcion.semestre}° Semestre)'
        )
        return redirect('inscripcionalumno:list')

    return render(request, 'inscripcion_alumno/confirm_delete.html', {'inscripcion': inscripcion})


def inscripcion_detail(request, pk):
    """Ver detalle de una inscripción"""
    inscripcion = get_object_or_404(InscripcionAlumno, pk=pk)
    return render(request, 'inscripcion_alumno/detail.html', {'inscripcion': inscripcion})
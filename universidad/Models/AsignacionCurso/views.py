from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import AsignacionCurso
from .forms import AsignacionCursoForm


def asignacion_list(request):
    """Listado de todas las asignaciones"""
    query = request.GET.get('q', '')
    asignaciones = AsignacionCurso.objects.select_related('curso', 'catedratico').all()

    if query:
        asignaciones = asignaciones.filter(
            models.Q(curso__nombre__icontains=query) |
            models.Q(curso__codigo__icontains=query) |
            models.Q(catedratico__nombre__icontains=query) |
            models.Q(catedratico__apellido__icontains=query) |
            models.Q(seccion__icontains=query)
        )

    return render(request, 'asignacion_curso/list.html', {
        'asignaciones': asignaciones,
        'query': query,
        'total_asignaciones': asignaciones.count()
    })


def asignacion_create(request):
    """Crear una nueva asignación"""
    if request.method == 'POST':
        form = AsignacionCursoForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
            messages.success(
                request,
                f'Asignación creada: {asignacion.curso.nombre} - {asignacion.catedratico.nombre} '
                f'{asignacion.catedratico.apellido} ({asignacion.anio} - {asignacion.semestre}° Sem - Secc {asignacion.seccion})'
            )
            return redirect('asignacioncurso:list')
    else:
        form = AsignacionCursoForm()

    return render(request, 'asignacion_curso/form.html', {
        'form': form,
        'title': 'Nueva Asignación de Curso',
        'button_text': 'Guardar Asignación'
    })


def asignacion_edit(request, pk):
    """Editar una asignación existente"""
    asignacion = get_object_or_404(AsignacionCurso, pk=pk)

    if request.method == 'POST':
        form = AsignacionCursoForm(request.POST, instance=asignacion)
        if form.is_valid():
            asignacion = form.save()
            messages.success(
                request,
                f'Asignación actualizada: {asignacion.curso.nombre} - {asignacion.catedratico.nombre} '
                f'{asignacion.catedratico.apellido} ({asignacion.anio} - {asignacion.semestre}° Sem - Secc {asignacion.seccion})'
            )
            return redirect('asignacioncurso:list')
    else:
        form = AsignacionCursoForm(instance=asignacion)

    return render(request, 'asignacion_curso/form.html', {
        'form': form,
        'title': f'Editar Asignación: {asignacion.curso.nombre} - Secc {asignacion.seccion}',
        'button_text': 'Actualizar Asignación',
        'asignacion': asignacion
    })


def asignacion_delete(request, pk):
    """Eliminar una asignación"""
    asignacion = get_object_or_404(AsignacionCurso, pk=pk)

    if request.method == 'POST':
        curso_nombre = asignacion.curso.nombre
        catedratico_nombre = f"{asignacion.catedratico.nombre} {asignacion.catedratico.apellido}"
        asignacion.delete()
        messages.success(
            request,
            f'Asignación eliminada: {curso_nombre} - {catedratico_nombre} '
            f'({asignacion.anio} - {asignacion.semestre}° Sem - Secc {asignacion.seccion})'
        )
        return redirect('asignacioncurso:list')

    return render(request, 'asignacion_curso/confirm_delete.html', {'asignacion': asignacion})


def asignacion_detail(request, pk):
    """Ver detalle de una asignación"""
    asignacion = get_object_or_404(AsignacionCurso, pk=pk)
    return render(request, 'asignacion_curso/detail.html', {'asignacion': asignacion})
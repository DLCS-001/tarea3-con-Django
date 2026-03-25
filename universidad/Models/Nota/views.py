from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import Nota
from .forms import NotaForm


def nota_list(request):
    """Listado de todas las calificaciones"""
    query = request.GET.get('q', '')
    notas = Nota.objects.select_related('alumno', 'curso').all()

    if query:
        notas = notas.filter(
            models.Q(alumno__first_name__icontains=query) |
            models.Q(alumno__last_name__icontains=query) |
            models.Q(curso__nombre__icontains=query) |
            models.Q(curso__codigo__icontains=query)
        )

    return render(request, 'nota/list.html', {
        'notas': notas,
        'query': query,
        'total_notas': notas.count()
    })


def nota_create(request):
    """Crear una nueva calificación"""
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, f'Calificación registrada correctamente para {nota.alumno} en {nota.curso}.')
            return redirect('nota:list')
    else:
        form = NotaForm()

    return render(request, 'nota/form.html', {
        'form': form,
        'title': 'Registrar Nueva Calificación',
        'button_text': 'Guardar Calificación'
    })


def nota_edit(request, pk):
    """Editar una calificación existente"""
    nota = get_object_or_404(Nota, pk=pk)

    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            nota = form.save()
            messages.success(request, f'Calificación actualizada correctamente para {nota.alumno} en {nota.curso}.')
            return redirect('nota:list')
    else:
        form = NotaForm(instance=nota)

    return render(request, 'nota/form.html', {
        'form': form,
        'title': f'Editar Calificación: {nota.alumno} - {nota.curso}',
        'button_text': 'Actualizar Calificación',
        'nota': nota
    })


def nota_delete(request, pk):
    """Eliminar una calificación"""
    nota = get_object_or_404(Nota, pk=pk)

    if request.method == 'POST':
        alumno_nombre = str(nota.alumno)
        curso_nombre = str(nota.curso)
        nota.delete()
        messages.success(request, f'Calificación eliminada correctamente para {alumno_nombre} en {curso_nombre}.')
        return redirect('nota:list')

    return render(request, 'nota/confirm_delete.html', {'nota': nota})


def nota_detail(request, pk):
    """Ver detalle de una calificación"""
    nota = get_object_or_404(Nota, pk=pk)
    return render(request, 'nota/detail.html', {'nota': nota})
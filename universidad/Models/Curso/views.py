from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import Curso
from .forms import CursoForm


def curso_list(request):
    query = request.GET.get('q', '')
    cursos = Curso.objects.all()

    if query:
        cursos = cursos.filter(
            models.Q(codigo__icontains=query) |
            models.Q(nombre__icontains=query) |
            models.Q(descripcion__icontains=query)
        )

    return render(request, 'curso/list.html', {
        'cursos': cursos,
        'query': query
    })


def curso_create(request):
    form = CursoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Curso registrado correctamente.')
        return redirect('curso:list')
    return render(request, 'curso/form.html', {
        'form': form,
        'title': 'Nuevo Curso'
    })


def curso_detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'curso/detail.html', {'curso': curso})


def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoForm(request.POST or None, instance=curso)
    if form.is_valid():
        form.save()
        messages.success(request, 'Curso actualizado correctamente.')
        return redirect('curso:list')
    return render(request, 'curso/form.html', {
        'form': form,
        'title': f'Editar: {curso.codigo} - {curso.nombre}'
    })


def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('curso:list')
    return render(request, 'curso/confirm_delete.html', {'curso': curso})
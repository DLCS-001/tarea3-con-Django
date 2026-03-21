from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from .models import Catedratico
from .forms import CatedraticoForm


def catedratico_list(request):
    query = request.GET.get('q', '')
    catedraticos = Catedratico.objects.all()

    if query:
        catedraticos = catedraticos.filter(
            models.Q(codigo__icontains=query) |
            models.Q(nombre__icontains=query) |
            models.Q(apellido__icontains=query) |
            models.Q(email__icontains=query)
        )

    return render(request, 'catedratico/list.html', {
        'catedraticos': catedraticos,
        'query': query
    })


def catedratico_create(request):
    if request.method == 'POST':
        form = CatedraticoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catedrático registrado correctamente.')
            return redirect('catedratico:list')
    else:
        form = CatedraticoForm()

    return render(request, 'catedratico/form.html', {
        'form': form,
        'title': 'Nuevo Catedrático'
    })


def catedratico_edit(request, pk):
    catedratico = get_object_or_404(Catedratico, pk=pk)

    if request.method == 'POST':
        form = CatedraticoForm(request.POST, instance=catedratico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catedrático actualizado correctamente.')
            return redirect('catedratico:list')
    else:
        form = CatedraticoForm(instance=catedratico)

    return render(request, 'catedratico/form.html', {
        'form': form,
        'title': f'Editar: {catedratico.nombre} {catedratico.apellido}'
    })


def catedratico_delete(request, pk):
    catedratico = get_object_or_404(Catedratico, pk=pk)

    if request.method == 'POST':
        catedratico.delete()
        messages.success(request, 'Catedrático eliminado correctamente.')
        return redirect('catedratico:list')

    return render(request, 'catedratico/confirm_delete.html', {'catedratico': catedratico})
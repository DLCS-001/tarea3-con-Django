from django.contrib import admin
from .models import AsignacionCurso

@admin.register(AsignacionCurso)
class AsignacionCursoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'catedratico', 'anio', 'semestre', 'seccion', 'created_at')
    list_filter = ('anio', 'semestre', 'curso')
    search_fields = ('curso__nombre', 'curso__codigo', 'catedratico__nombre', 'catedratico__apellido', 'seccion')
    ordering = ('-anio', '-semestre', 'curso__nombre')
    fieldsets = (
        ('Información de Asignación', {
            'fields': ('curso', 'catedratico')
        }),
        ('Período Académico', {
            'fields': ('anio', 'semestre', 'seccion')
        }),
        ('Fecha de Creación', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
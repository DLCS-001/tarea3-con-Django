from django.contrib import admin
from .models import InscripcionAlumno

@admin.register(InscripcionAlumno)
class InscripcionAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'anio', 'semestre', 'estado', 'fecha_inscripcion')
    list_filter = ('estado', 'anio', 'semestre', 'curso')
    search_fields = ('alumno__first_name', 'alumno__last_name', 'alumno__carnet', 'curso__nombre', 'curso__codigo')
    ordering = ('-fecha_inscripcion',)
    fieldsets = (
        ('Información del Alumno', {
            'fields': ('alumno', 'curso')
        }),
        ('Período Académico', {
            'fields': ('anio', 'semestre')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Fecha de Inscripción', {
            'fields': ('fecha_inscripcion',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('fecha_inscripcion',)
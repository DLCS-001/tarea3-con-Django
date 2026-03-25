from django.contrib import admin
from .models import Nota

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'zona', 'examen_final', 'nota_final', 'created_at')
    list_filter = ('curso', 'created_at')
    search_fields = ('alumno__first_name', 'alumno__last_name', 'curso__nombre', 'curso__codigo')
    readonly_fields = ('zona', 'nota_final', 'created_at', 'updated_at')
    fieldsets = (
        ('Información del Estudiante', {
            'fields': ('alumno', 'curso')
        }),
        ('Calificaciones', {
            'fields': ('nota1', 'nota2', 'nota3', 'examen_final')
        }),
        ('Resultados (Calculados)', {
            'fields': ('zona', 'nota_final'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
from django.contrib import admin

from .models import Alumno


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('carnet', 'first_name', 'last_name', 'email', 'is_active')
    list_filter = ('is_active', 'gender')
    search_fields = ('carnet', 'first_name', 'last_name', 'email')
    ordering = ('carnet',)

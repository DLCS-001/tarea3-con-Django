from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'creditos', 'is_active')
    list_filter = ('is_active', 'creditos')
    search_fields = ('codigo', 'nombre')
    ordering = ('codigo',)
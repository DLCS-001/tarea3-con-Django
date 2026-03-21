from django.contrib import admin
from .models import Catedratico

@admin.register(Catedratico)
class CatedraticoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'apellido', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('codigo', 'nombre', 'apellido', 'email')
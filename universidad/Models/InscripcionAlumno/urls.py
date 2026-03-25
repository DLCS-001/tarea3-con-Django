from django.urls import path
from . import views

app_name = 'inscripcionalumno'

urlpatterns = [
    path('', views.inscripcion_list, name='list'),
    path('nuevo/', views.inscripcion_create, name='create'),
    path('<int:pk>/', views.inscripcion_detail, name='detail'),
    path('<int:pk>/editar/', views.inscripcion_edit, name='edit'),
    path('<int:pk>/eliminar/', views.inscripcion_delete, name='delete'),
]
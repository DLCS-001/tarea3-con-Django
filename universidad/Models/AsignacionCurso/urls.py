from django.urls import path
from . import views

app_name = 'asignacioncurso'

urlpatterns = [
    path('', views.asignacion_list, name='list'),
    path('nuevo/', views.asignacion_create, name='create'),
    path('<int:pk>/', views.asignacion_detail, name='detail'),
    path('<int:pk>/editar/', views.asignacion_edit, name='edit'),
    path('<int:pk>/eliminar/', views.asignacion_delete, name='delete'),
]
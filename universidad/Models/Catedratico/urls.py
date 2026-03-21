from django.urls import path
from . import views

app_name = 'catedratico'

urlpatterns = [
    path('', views.catedratico_list, name='list'),
    path('nuevo/', views.catedratico_create, name='create'),
    path('<int:pk>/editar/', views.catedratico_edit, name='edit'),
    path('<int:pk>/eliminar/', views.catedratico_delete, name='delete'),
]
from django.urls import path
from . import views

app_name = 'curso'

urlpatterns = [
    path('', views.curso_list, name='list'),
    path('nuevo/', views.curso_create, name='create'),
    path('<int:pk>/', views.curso_detail, name='detail'),
    path('<int:pk>/editar/', views.curso_edit, name='edit'),
    path('<int:pk>/eliminar/', views.curso_delete, name='delete'),
]
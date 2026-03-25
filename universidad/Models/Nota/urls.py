from django.urls import path
from . import views

app_name = 'nota'

urlpatterns = [
    path('', views.nota_list, name='list'),
    path('nuevo/', views.nota_create, name='create'),
    path('<int:pk>/', views.nota_detail, name='detail'),
    path('<int:pk>/editar/', views.nota_edit, name='edit'),
    path('<int:pk>/eliminar/', views.nota_delete, name='delete'),
]
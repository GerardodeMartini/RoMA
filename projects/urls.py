from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('proyectos/', views.project_list, name='project_list'),
    path('proyectos/<int:pk>/', views.project_detail, name='project_detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos_hub, name='productos_hub'),
    path('productos/revestimientos/', views.porcelanatos, name='porcelanatos'),
    path('productos/prefabricados-hormigon/', views.productos_hormigon, name='productos_hormigon'),
    path('proyectos/', views.project_list, name='project_list'),
    path('proyectos/<int:pk>/', views.project_detail, name='project_detail'),
    path('edicion/', views.edicion, name='edicion'),
    path('edicion/nuevo-proyecto/', views.add_project, name='add_project'),
    path('edicion/gestionar-proyectos/', views.manage_projects, name='manage_projects'),
    path('edicion/proyectos/<int:pk>/editar/', views.edit_project, name='edit_project'),
    path('edicion/nuevo-porcelanato/', views.add_porcelanato, name='add_porcelanato'),
    path('edicion/gestionar-porcelanatos/', views.manage_porcelanatos, name='manage_porcelanatos'),
    path('edicion/porcelanatos/<int:pk>/editar/', views.edit_porcelanato, name='edit_porcelanato'),
    path('edicion/porcelanatos/<int:pk>/eliminar/', views.delete_porcelanato, name='delete_porcelanato'),
    path('edicion/proyectos/<int:pk>/eliminar/', views.delete_project, name='delete_project'),
    path('edicion/gestionar-hormigon/', views.manage_hormigones, name='manage_hormigones'),
    path('edicion/nuevo-hormigon/', views.add_hormigon, name='add_hormigon'),
    path('edicion/hormigon/<int:pk>/editar/', views.edit_hormigon, name='edit_hormigon'),
    path('edicion/hormigon/<int:pk>/eliminar/', views.delete_hormigon, name='delete_hormigon'),
]

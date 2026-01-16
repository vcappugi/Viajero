from django.urls import path
from . import views

app_name = 'viaticos'

urlpatterns = [
    path('', views.home, name='home'),
    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresas/nueva/', views.empresa_create, name='empresa_create'),
    path('empresas/editar/<int:pk>/', views.empresa_update, name='empresa_update'),
    path('empresas/inactivar/<int:pk>/', views.empresa_inactivate, name='empresa_inactivate'),
    # Usuarios
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/nuevo/', views.user_create, name='user_create'),
    path('usuarios/editar/<int:pk>/', views.user_update, name='user_update'),
    path('usuarios/toggle/<int:pk>/', views.user_toggle_status, name='user_toggle_status'),
    path('logout/', views.custom_logout, name='custom_logout'),

    # Roles
    path('roles/', views.role_list, name='role_list'),
    path('roles/nuevo/', views.role_create, name='role_create'),
    path('roles/editar/<int:pk>/', views.role_update, name='role_update'),
    path('roles/toggle/<int:pk>/', views.role_toggle_status, name='role_toggle_status'),

    # Tasas de Cambio
    path('tasas/', views.tasa_list, name='tasa_list'),
    path('tasas/nueva/', views.tasa_create, name='tasa_create'),
    path('tasas/editar/<int:pk>/', views.tasa_update, name='tasa_update'),

    # Localidades
    path('localidades/', views.localidad_list, name='localidad_list'),
    path('localidades/nueva/', views.localidad_create, name='localidad_create'),
    path('localidades/editar/<int:pk>/', views.localidad_update, name='localidad_update'),

    # Tipos de Viáticos
    path('viaticos/tipos/', views.tipo_viatico_list, name='tipo_viatico_list'),
    path('viaticos/tipos/nuevo/', views.tipo_viatico_create, name='tipo_viatico_create'),
    path('viaticos/tipos/editar/<int:pk>/', views.tipo_viatico_update, name='tipo_viatico_update'),
    path('viaticos/tipos/toggle/<int:pk>/', views.tipo_viatico_toggle_status, name='tipo_viatico_toggle_status'),

    # Solicitudes
    path('solicitudes/', views.solicitud_list, name='solicitud_list'),
    path('solicitudes/nueva/', views.solicitud_create, name='solicitud_create'),
    path('solicitudes/editar/<int:pk>/', views.solicitud_update, name='solicitud_update'),
    path('solicitudes/detalle/<int:pk>/', views.solicitud_detalle, name='solicitud_detalle'),
    path('solicitudes/aprobar/<int:pk>/', views.solicitud_aprobar, name='solicitud_aprobar'),
    path('solicitudes/cambiar-estado/<int:pk>/', views.solicitud_cambiar_estado, name='solicitud_cambiar_estado'),
]

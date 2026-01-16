from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Roles, Empresa, UserProfile, TasaCambio, Localidad, TipoViatico, Banco

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('codigo_bco', 'nombre_banco', 'descripcion')
    search_fields = ('codigo_bco', 'nombre_banco')

# Inline para el perfil de usuario
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'user'

# Extendiendo el UserAdmin de Django
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

# Re-registrar User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol', 'empresa', 'tipo_rol', 'fecha_creacion', 'creadopor', 'actualizadopor')
    list_filter = ('empresa', 'tipo_rol', 'creadopor')
    search_fields = ('nombre_rol', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creadopor', 'actualizadopor')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creadopor = request.user
        obj.actualizadopor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'fecha_creacion', 'creadopor', 'actualizadopor')
    search_fields = ('nombre', 'descripcion', 'direccion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creadopor', 'actualizadopor')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creadopor = request.user
        obj.actualizadopor = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cedula_identidad', 'nombre_completo', 'empresa', 'rol', 'banco', 'fecha_creacion', 'creadopor')
    list_filter = ('empresa', 'rol', 'banco', 'creadopor')
    search_fields = ('user__username', 'cedula_identidad', 'nombre_completo', 'user__email', 'nro_cuenta', 'Telefono_pagomovil')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creadopor', 'actualizadopor')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creadopor = request.user
        obj.actualizadopor = request.user
        super().save_model(request, obj, form, change)

@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = ('fecha_valor', 'tasa_dolar', 'fecha_creacion', 'creadopor', 'actualizadopor')
    list_filter = ('creadopor', 'fecha_valor')
    search_fields = ('fecha_valor',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creadopor', 'actualizadopor')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creadopor = request.user
        obj.actualizadopor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'es_premium', 'fecha_creacion', 'creadopor')
    list_filter = ('zona', 'es_premium', 'creadopor')
    search_fields = ('nombre', 'zona')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creadopor', 'actualizadopor')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creadopor = request.user
        obj.actualizadopor = request.user
        super().save_model(request, obj, form, change)

@admin.register(TipoViatico)
class TipoViaticoAdmin(admin.ModelAdmin):
    list_display = ('tipo_gasto', 'es_premium', 'montodolares', 'gestionadicional', 'activo', 'fecha_creacion', 'creadopor')
    list_filter = ('es_premium', 'gestionadicional', 'activo', 'creadopor')
    search_fields = ('tipo_gasto',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'creadopor', 'actualizadopor')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creadopor = request.user
        obj.actualizadopor = request.user
        super().save_model(request, obj, form, change)

from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Empresa, UserProfile, Roles, TasaCambio, 
    Localidad, TipoViatico, Solicitud, SolicitudDetalle
)
from django.contrib.auth.models import User

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion', 'direccion', 'telefono', 'logo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary text-lg',
                'placeholder': 'Nombre de la empresa'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered h-24 w-full focus:textarea-primary',
                'placeholder': 'Breve descripción de la empresa'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Dirección física'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Ej. +58 212 0000000'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full focus:file-input-primary',
                'accept': 'image/*'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Empresa',
            'descripcion': 'Descripción',
            'direccion': 'Dirección Física',
            'telefono': 'Teléfono de Contacto',
            'logo': 'Logo de la Empresa',
            'activo': 'Empresa Activa'
        }

class ExtendedUserForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full focus:input-primary',
        'placeholder': 'Dejar en blanco para no cambiar'
    }), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full focus:input-primary'}),
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox checkbox-primary'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Primer Nombre',
            'last_name': 'Apellidos',
            'is_active': 'Usuario Activo',
        }

class UserProfileForm(forms.ModelForm):
    foto = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered w-full focus:file-input-primary',
            'accept': 'image/*'
        }),
        label='Foto del Usuario',
        help_text='Tamaño máximo: 2MB. Formatos: JPG, PNG, GIF'
    )
    
    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            # Validar tamaño máximo de 2MB (2 * 1024 * 1024 bytes)
            max_size = 2 * 1024 * 1024
            if foto.size > max_size:
                raise ValidationError('La imagen no puede ser mayor a 2MB. Tamaño actual: {:.2f}MB'.format(foto.size / (1024 * 1024)))
        return foto
    
    class Meta:
        model = UserProfile
        fields = ['cedula_identidad', 'foto', 'nombre_completo', 'telefono', 'empresa', 'rol', 'supervisor', 'banco', 'nro_cuenta', 'Telefono_pagomovil', 'descripcion']
        widgets = {
            'cedula_identidad': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary', 'placeholder': 'Ej: V-12345678'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary'}),
            'telefono': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary', 'placeholder': 'WhatsApp'}),
            'empresa': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'rol': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'supervisor': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'banco': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'nro_cuenta': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary', 'placeholder': '20 dígitos'}),
            'Telefono_pagomovil': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary', 'placeholder': '04XX-1234567'}),
            'descripcion': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full focus:textarea-primary', 'rows': 2}),
        }
        labels = {
            'cedula_identidad': 'Cédula de Identidad',
            'foto': 'Foto del Usuario',
            'nombre_completo': 'Nombre Completo / Firma',
            'telefono': 'Número de Contacto (WhatsApp)',
            'empresa': 'Empresa Asignada',
            'rol': 'Rol en el Sistema',
            'supervisor': 'Supervisor Directo',
            'banco': 'Banco Destinatario',
            'nro_cuenta': 'Número de Cuenta Bancaria',
            'Telefono_pagomovil': 'Teléfono asociado a Pago Móvil',
            'descripcion': 'Notas Adicionales',
        }

class RoleForm(forms.ModelForm):
    # ... previous meta and labels ...
    class Meta:
        model = Roles
        fields = ['empresa', 'nombre_rol', 'tipo_rol', 'descripcion']
        widgets = {
            'empresa': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'nombre_rol': forms.TextInput(attrs={'class': 'input input-bordered w-full focus:input-primary'}),
            'tipo_rol': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'descripcion': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full focus:textarea-primary', 'rows': 3}),
        }
        labels = {
            'empresa': 'Empresa',
            'nombre_rol': 'Nombre del Rol',
            'tipo_rol': 'Tipo de Rol (Nivel de Acceso)',
            'descripcion': 'Descripción de Responsabilidades',
        }



class TasaCambioForm(forms.ModelForm):
    # ... previous meta and labels ...
    class Meta:
        model = TasaCambio
        fields = ['fecha_valor', 'tasa_dolar']
        widgets = {
            'fecha_valor': forms.DateInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'type': 'date'
            }),
            'tasa_dolar': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Ej. 36.50',
                'step': '0.0001'
            }),
        }
        labels = {
            'fecha_valor': 'Fecha de la Tasa',
            'tasa_dolar': 'Valor del Dólar (Bs.)',
        }

class LocalidadForm(forms.ModelForm):
    # ... previous meta and labels ...
    class Meta:
        model = Localidad
        fields = ['nombre', 'zona', 'es_premium']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Ej. Caracas, Valencia, etc.'
            }),
            'zona': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Ej. Capital, Central, Occidente...'
            }),
            'es_premium': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Localidad',
            'zona': 'Zona / Región',
            'es_premium': 'Tarifa Premium (Aplica recargo)',
        }

class TipoViaticoForm(forms.ModelForm):
    class Meta:
        model = TipoViatico
        fields = ['tipo_gasto', 'es_premium', 'montodolares', 'gestionadicional', 'activo']
        widgets = {
            'tipo_gasto': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Ej. Desayuno, Almuerzo, Taxi...'
            }),
            'es_premium': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
            'montodolares': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full focus:input-primary',
                'placeholder': 'Monto en USD',
                'step': '0.01'
            }),
            'gestionadicional': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
        }
        labels = {
            'tipo_gasto': 'Descripción del Gasto',
            'es_premium': 'Aplica Tarifa Premium',
            'montodolares': 'Monto en Dólares ($)',
            'gestionadicional': 'Gestión Adicional (Varios Días)',
            'activo': 'Gasto Activo',
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['solicitante', 'empresa', 'fecha_solicitud', 'cantidad_personas', 'estado_solicitud', 'desde', 'hasta', 'descripcion', 'localidad']
        widgets = {
            'solicitante': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'empresa': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'fecha_solicitud': forms.DateInput(attrs={'class': 'input input-bordered w-full focus:select-primary', 'type': 'date'}),
            'cantidad_personas': forms.NumberInput(attrs={'class': 'input input-bordered w-full focus:select-primary', 'min': 1}),
            'estado_solicitud': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'desde': forms.DateInput(attrs={'class': 'input input-bordered w-full focus:select-primary', 'type': 'date'}),
            'hasta': forms.DateInput(attrs={'class': 'input input-bordered w-full focus:select-primary', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full focus:textarea-primary', 'rows': 2}),
            'localidad': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
        }
        labels = {
            'solicitante': 'Usuario Beneficiario',
            'empresa': 'Empresa',
            'fecha_solicitud': 'Fecha de Solicitud',
            'cantidad_personas': 'Cantidad de Personas',
            'estado_solicitud': 'Estado de la Solicitud',
            'desde': 'Fecha desde',
            'hasta': 'Fecha hasta',
            'descripcion': 'Descripción',
            'localidad': 'Destino del Viaje',
        }

class SolicitudDetalleForm(forms.ModelForm):
    class Meta:
        model = SolicitudDetalle
        fields = ['tipo_viatico', 'cantidad']
        widgets = {
            'tipo_viatico': forms.Select(attrs={'class': 'select select-bordered w-full focus:select-primary'}),
            'cantidad': forms.NumberInput(attrs={'class': 'input input-bordered w-full focus:input-primary', 'min': 1}),
        }
        labels = {
            'tipo_viatico': 'Concepto de Gasto',
            'cantidad': 'Cantidad',
        }

SolicitudDetalleFormSet = forms.inlineformset_factory(
    Solicitud, SolicitudDetalle, form=SolicitudDetalleForm,
    extra=1, can_delete=True
)

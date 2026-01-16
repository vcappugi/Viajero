from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Empresa(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='', blank=True, null=True, verbose_name='Logo de la Empresa')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresas_creadas')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresas_actualizadas')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Sistema"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def descripcion_corta(self):
        if not self.descripcion:
            return "Sin descripción"
        if len(self.descripcion) > 50:
            return f"{self.descripcion[:47]}..."
        return self.descripcion

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Empresas"

class Roles(models.Model):
    TIPO_ROL_CHOICES = [
        ('USUARIO', 'Usuario'),
        ('APROBADOR', 'Aprobador Administrativo'),
        ('GESTIONADOR', 'Gestionador de Servicios'),
        ('ADMINISTRADOR', 'Administrador del Sistema'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='roles', null=True, blank=True)
    nombre_rol = models.CharField(max_length=100)
    tipo_rol = models.CharField(max_length=20, choices=TIPO_ROL_CHOICES, default='USUARIO')
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='roles_creados')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='roles_actualizados')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Sistema"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def descripcion_corta(self):
        if not self.descripcion:
            return "Sin descripción"
        if len(self.descripcion) > 60:
            return f"{self.descripcion[:57]}..."
        return self.descripcion

    def __str__(self):
        return f"{self.nombre_rol} ({self.empresa.nombre})"

    class Meta:
        verbose_name_plural = "Roles"
        unique_together = ('empresa', 'nombre_rol')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nombre_completo = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True, help_text="Número de WhatsApp")
    descripcion = models.TextField(blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados')
    rol = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinados')
    
    # Datos de pago e identificación
    cedula_identidad = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cédula de Identidad")
    foto = models.ImageField(upload_to='', blank=True, null=True, verbose_name='Foto del Usuario')
    banco = models.ForeignKey('Banco', on_delete=models.SET_NULL, null=True, blank=True, related_name='perfiles_bancarios', verbose_name="Banco")
    nro_cuenta = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de Cuenta")
    Telefono_pagomovil = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono Pago Móvil")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='perfiles_creados')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='perfiles_actualizados')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Admin"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    def __str__(self):
        return f"{self.user.username} - {self.nombre_completo or self.user.get_full_name()}"

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

class TasaCambio(models.Model):
    fecha_valor = models.DateField(unique=True, help_text="Fecha a la que corresponde esta tasa")
    tasa_dolar = models.DecimalField(max_digits=12, decimal_places=4, help_text="Valor del dólar en bolívares")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasas_creadas')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasas_actualizadas')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Sistema"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    def __str__(self):
        return f"{self.fecha_valor}: {self.tasa_dolar}"

    class Meta:
        verbose_name = "Tasa de Cambio"
        verbose_name_plural = "Tasas de Cambio"
        ordering = ['-fecha_valor']

class Localidad(models.Model):
    nombre = models.CharField(max_length=255, unique=True, help_text="Nombre de la localidad (Ciudad/Estado)")
    zona = models.CharField(max_length=100, help_text="Zona o región geográfica")
    es_premium = models.BooleanField(default=False, help_text="Indica si aplica tarifa especial Premium")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='localidades_creadas')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='localidades_actualizadas')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Sistema"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    def __str__(self):
        return f"{self.nombre} ({self.zona})"

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"
        ordering = ['nombre']

class TipoViatico(models.Model):
    tipo_gasto = models.CharField(max_length=100, unique=True, help_text="Ej: Alimentación, Transporte, Alojamiento...")
    es_premium = models.BooleanField(default=False, help_text="Indica si aplica para tarifa Premium")
    montodolares = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto base en USD")
    gestionadicional = models.BooleanField(default=False, help_text="Indica si requiere gestión adicional")
    activo = models.BooleanField(default=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tipos_viaticos_creados')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tipos_viaticos_actualizados')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Sistema"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    def __str__(self):
        return f"{self.tipo_gasto} ({'Premium' if self.es_premium else 'Normal'})"

    class Meta:
        verbose_name = "Tipo de Viático"
        verbose_name_plural = "Tipos de Viáticos"
        ordering = ['tipo_gasto']

class Banco(models.Model):
    codigo_bco = models.CharField(max_length=10, unique=True, verbose_name="Código del Banco", help_text="Ej: 0102, 0105...")
    nombre_banco = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Banco")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre_banco

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"
        ordering = ['nombre_banco']


class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('NUEVO', 'Nuevo'),
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('EN_GESTION', 'En Gestión'),
        ('COMPLETADO', 'Completado'),
        ('RELACIONADO', 'Relacionado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    nro_solicitud = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='solicitudes_empresa', null=True, blank=True)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_realizadas')
    aprobador_administrativo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_por_aprobar')
    fecha_solicitud = models.DateField(default=timezone.now)
    desde = models.DateField(default=timezone.now)
    hasta = models.DateField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)   
    estado_solicitud = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='NUEVO')
    cantidad_personas = models.PositiveIntegerField(default=1)
    total_dolares = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_bolivares = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_localidad')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='solicitudes_creadas')
    actualizadopor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='solicitudes_actualizadas')

    @property
    def audit_creacion(self):
        user = self.creadopor.username if self.creadopor else "Sistema"
        date = self.fecha_creacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    @property
    def audit_modifica(self):
        user = self.actualizadopor.username if self.actualizadopor else "-"
        date = self.fecha_actualizacion.strftime("%d/%m/%y %H:%M")
        return f"{user} ({date})"

    def __str__(self):
        return f"Solicitud #{self.nro_solicitud} - {self.solicitante.username}"

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ['-nro_solicitud']

class SolicitudDetalle(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='detalles')
    tipo_viatico = models.ForeignKey(TipoViatico, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    monto_dolares = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Detalle #{self.solicitud.nro_solicitud} - {self.tipo_viatico.tipo_gasto}"

    class Meta:
        verbose_name = "Detalle de Solicitud"
        verbose_name_plural = "Detalles de Solicitudes"

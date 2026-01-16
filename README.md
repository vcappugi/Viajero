# VIAJERO - Sistema de Gestión y Aprobación de Viáticos

![Django](https://img.shields.io/badge/Django-6.0.1-green)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.4.2-38bdf8)

Sistema web completo para la gestión, aprobación y seguimiento de viáticos empresariales. Automatiza el ciclo de vida completo de los viáticos, desde la solicitud inicial hasta la rendición de cuentas final.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelos de Datos](#-modelos-de-datos)
- [Roles y Permisos](#-roles-y-permisos)
- [Desarrollo](#-desarrollo)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🔐 Gestión de Usuarios y Seguridad
- Sistema de autenticación con Django
- Control de acceso basado en roles (RBAC)
- Perfiles de usuario con información completa
- Jerarquía de supervisión
- Gestión de empresas y logos

### 📝 Solicitudes de Viáticos
- Formulario intuitivo para crear solicitudes
- Cálculo automático de montos en USD y Bs.
- Integración con tasas de cambio
- Gestión de localidades y destinos
- Tipos de viáticos configurables (Alimentación, Transporte, Alojamiento)
- Vista previa y edición de solicitudes

### ✅ Aprobación y Revisión
- Panel de aprobación para administradores
- Modal de revisión con información completa
- Aprobación o rechazo de solicitudes
- Historial de cambios y auditoría
- Notificaciones automáticas

### 📊 Gestión y Reportes
- Listado de solicitudes con filtros
- Resumen de montos y estados
- Exportación a PDF
- Trazabilidad completa de operaciones

### 🎨 Interfaz de Usuario
- Diseño moderno con TailwindCSS y DaisyUI
- Interfaz responsive (mobile-first)
- Modales y componentes interactivos
- Experiencia de usuario optimizada

## 🛠 Tecnologías

### Backend
- **Django 6.0.1** - Framework web de alto nivel
- **PostgreSQL** - Base de datos relacional
- **Python 3.14** - Lenguaje de programación

### Frontend
- **TailwindCSS 4.4.2** - Framework CSS utility-first
- **DaisyUI** - Componentes para TailwindCSS
- **Font Awesome 6** - Iconografía

### Herramientas
- **django-tailwind** - Integración de TailwindCSS con Django
- **django-browser-reload** - Recarga automática en desarrollo
- **psycopg2-binary** - Adaptador PostgreSQL para Python

## 📦 Requisitos

- Python 3.14 o superior
- PostgreSQL 15 o superior
- pip (gestor de paquetes de Python)
- Node.js y npm (para TailwindCSS)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd VIAJERO
```

### 2. Crear entorno virtual

```bash
cd VIAJERO
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear una base de datos PostgreSQL:

```sql
CREATE DATABASE viajero;
CREATE USER viajeroadm WITH PASSWORD 'viajero adm';
ALTER ROLE viajeroadm SET client_encoding TO 'utf8';
ALTER ROLE viajeroadm SET default_transaction_isolation TO 'read committed';
ALTER ROLE viajeroadm SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE viajero TO viajeroadm;
```

### 5. Configurar variables de entorno

Editar `VIAJERO/Viajero/Viajero/settings.py` con tus configuraciones:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'viajero',
        'USER': 'viajeroadm',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Ejecutar migraciones

```bash
cd VIAJERO/Viajero
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Instalar y compilar TailwindCSS

```bash
python manage.py tailwind install
python manage.py tailwind build
```

### 9. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en `http://127.0.0.1:8000/`

## ⚙️ Configuración

### Archivos de Media

Las imágenes (logos de empresas y fotos de usuarios) se almacenan en:
- `VIAJERO/Viajero/static/images/`

Asegúrate de que este directorio tenga permisos de escritura.

### Configuración de Media URL

En `settings.py`:
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'static' / 'images'
```

### Configuración de Static Files

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

## 📖 Uso

### Acceso al Sistema

1. Navega a `http://127.0.0.1:8000/`
2. Inicia sesión con tus credenciales
3. El sistema redirigirá según tu rol

### Crear una Solicitud

1. Desde el home, haz clic en "Nueva Solicitud"
2. Completa el formulario:
   - Selecciona el solicitante (por defecto: usuario logueado)
   - Ingresa fechas de viaje
   - Selecciona localidad/destino
   - Agrega conceptos de gastos
3. El sistema calculará automáticamente los montos
4. Guarda la solicitud

### Aprobar/Rechazar Solicitud

1. Desde el home, en la lista de solicitudes
2. Haz clic en "Revisar" (solo visible para aprobadores)
3. Revisa la información en el modal
4. Selecciona "Aprobar" o "Rechazar"
5. Confirma la acción

### Ver Detalles de Solicitud

1. Haz clic en "Detalles" en cualquier solicitud
2. Se abrirá un modal con información completa
3. Puedes imprimir en PDF desde el modal

## 📁 Estructura del Proyecto

```
VIAJERO/
├── Documentacion/          # Documentación del proyecto
│   ├── PDR_VIAJERO.md       # Product Requirements Document
│   └── promt inicial.md     # Prompt inicial del proyecto
│
├── VIAJERO/
│   ├── Viajero/             # Aplicación principal Django
│   │   ├── manage.py
│   │   ├── Viajero/         # Configuración del proyecto
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── asgi.py
│   │   │
│   │   ├── viaticos/        # Aplicación principal
│   │   │   ├── models.py    # Modelos de datos
│   │   │   ├── views.py     # Vistas y lógica de negocio
│   │   │   ├── forms.py     # Formularios
│   │   │   ├── urls.py      # Rutas de la aplicación
│   │   │   ├── admin.py     # Configuración del admin
│   │   │   └── migrations/  # Migraciones de base de datos
│   │   │
│   │   ├── theme/           # Tema TailwindCSS
│   │   │   └── static_src/  # Archivos fuente de Tailwind
│   │   │
│   │   ├── templates/       # Plantillas HTML
│   │   │   ├── base.html
│   │   │   ├── registration/
│   │   │   └── viaticos/
│   │   │
│   │   └── static/          # Archivos estáticos
│   │       ├── images/      # Imágenes subidas (logos, fotos)
│   │       └── img/          # Imágenes del sistema
│   │
│   ├── requirements.txt     # Dependencias Python
│   └── venv/                # Entorno virtual (no versionado)
│
└── README.md               # Este archivo
```

## 🗄 Modelos de Datos

### Principales

- **Empresa**: Información de empresas con logos
- **UserProfile**: Perfiles extendidos de usuarios con fotos
- **Roles**: Sistema de roles y permisos
- **Localidad**: Catálogo de destinos de viaje
- **TipoViatico**: Tipos de gastos configurables
- **TasaCambio**: Tasas de cambio USD/Bs. históricas
- **Solicitud**: Solicitudes de viáticos
- **SolicitudDetalle**: Detalle de conceptos por solicitud
- **Banco**: Catálogo de bancos

### Estados de Solicitud

- `NUEVO`: Solicitud recién creada
- `SOLICITADO`: Solicitud enviada para aprobación
- `APROBADO`: Solicitud aprobada
- `EN_GESTION`: En proceso de gestión logística
- `COMPLETADO`: Viaje completado
- `RELACIONADO`: Relacionado con otra solicitud
- `RECHAZADO`: Solicitud rechazada

## 👥 Roles y Permisos

### Usuario (Solicitante)
- Crear y editar sus propias solicitudes
- Ver sus solicitudes
- Cargar comprobantes de rendición

### Aprobador Administrativo
- Ver solicitudes pendientes de aprobación
- Aprobar o rechazar solicitudes
- Revisar rendiciones de cuentas

### Gestionador de Servicios
- Gestionar logística de viajes aprobados
- Coordinar traslados y hospedajes

### Administrador del Sistema
- Gestión completa de usuarios
- Configuración de parámetros del sistema
- Acceso a todos los módulos

## 🛠 Desarrollo

### Ejecutar en modo desarrollo

```bash
python manage.py runserver
```

### Compilar TailwindCSS en modo watch

```bash
python manage.py tailwind start
```

### Crear migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Acceder al admin de Django

```
http://127.0.0.1:8000/admin/
```

### Ejecutar tests

```bash
python manage.py test
```

## 📝 Notas de Desarrollo

### Características Implementadas

✅ Sistema de autenticación y autorización  
✅ Gestión de usuarios con perfiles extendidos  
✅ CRUD completo de empresas con logos  
✅ CRUD completo de usuarios con fotos  
✅ Gestión de roles y permisos  
✅ Catálogo de localidades  
✅ Tipos de viáticos configurables  
✅ Tasas de cambio históricas  
✅ Solicitudes de viáticos con detalles  
✅ Cálculo automático de montos  
✅ Panel de aprobación/rechazo  
✅ Modales de detalles y revisión  
✅ Exportación a PDF  
✅ Interfaz responsive con TailwindCSS  

### Próximas Funcionalidades

🔄 Gestión logística completa  
🔄 Rendición de cuentas post-viaje  
🔄 Sistema de notificaciones (Email/WhatsApp)  
🔄 Reportes avanzados  
🔄 Dashboard con métricas  

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Seguir PEP 8 para Python
- Documentar funciones complejas
- Escribir tests para nuevas funcionalidades
- Mantener el código limpio y legible

## 📄 Licencia

Este proyecto es privado y de uso interno.

## 👤 Autor

**Victor Cappugi**

## 📞 Soporte

Para soporte, contacta al equipo de desarrollo o abre un issue en el repositorio.

---

**VIAJERO** - Simplificando la gestión de viáticos empresariales 🚀

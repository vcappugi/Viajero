from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Empresa, UserProfile, Roles, TasaCambio, Localidad, TipoViatico, Solicitud, SolicitudDetalle
from .forms import (
    EmpresaForm, ExtendedUserForm, UserProfileForm, RoleForm, 
    TasaCambioForm, LocalidadForm, TipoViaticoForm, 
    SolicitudForm, SolicitudDetalleFormSet
)
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum, Q

@login_required
def home(request):
    # Obtener solicitudes donde el usuario es solicitante o aprobador
    solicitudes = Solicitud.objects.filter(
        (Q(solicitante=request.user) | Q(aprobador_administrativo=request.user)) & Q(estado_solicitud='SOLICITADO')
    ).select_related('solicitante', 'aprobador_administrativo', 'localidad').order_by('-nro_solicitud')[:10]
    
    return render(request, 'viaticos/home.html', {
        'solicitudes': solicitudes
    })

@login_required
def solicitud_detalle(request, pk):
    """Vista para mostrar los detalles de una solicitud en un modal"""
    solicitud = get_object_or_404(
        Solicitud.objects.select_related('solicitante', 'aprobador_administrativo', 'localidad'),
        pk=pk
    )
    
    # Verificar que el usuario tenga permiso para ver esta solicitud
    if solicitud.solicitante != request.user and solicitud.aprobador_administrativo != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para ver esta solicitud")
    
    # Obtener los detalles de la solicitud
    detalles = solicitud.detalles.select_related('tipo_viatico').all()
    
    return render(request, 'viaticos/solicitud_detalle.html', {
        'solicitud': solicitud,
        'detalles': detalles
    })

@login_required
def solicitud_aprobar(request, pk):
    """Vista para mostrar el modal de aprobación/rechazo"""
    solicitud = get_object_or_404(
        Solicitud.objects.select_related('solicitante', 'aprobador_administrativo', 'localidad'),
        pk=pk
    )
    
    # Verificar que el usuario sea el aprobador administrativo
    if solicitud.aprobador_administrativo != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para aprobar esta solicitud")
    
    return render(request, 'viaticos/solicitud_aprobar.html', {
        'solicitud': solicitud
    })

@login_required
def solicitud_cambiar_estado(request, pk):
    """Vista para cambiar el estado de una solicitud (aprobar o rechazar)"""
    from django.http import JsonResponse
    
    solicitud = get_object_or_404(Solicitud, pk=pk)
    
    # Verificar que el usuario sea el aprobador administrativo
    if solicitud.aprobador_administrativo != request.user:
        return JsonResponse({'success': False, 'error': 'No tienes permiso para cambiar el estado de esta solicitud'}, status=403)
    
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        accion = data.get('accion')
        
        if accion == 'aprobar':
            solicitud.estado_solicitud = 'APROBADO'
            solicitud.actualizadopor = request.user
            solicitud.save()
            return JsonResponse({'success': True, 'message': 'Solicitud aprobada correctamente'})
        elif accion == 'rechazar':
            solicitud.estado_solicitud = 'RECHAZADO'
            solicitud.actualizadopor = request.user
            solicitud.save()
            return JsonResponse({'success': True, 'message': 'Solicitud rechazada correctamente'})
        else:
            return JsonResponse({'success': False, 'error': 'Acción no válida'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def empresa_list(request):
    # Obtener el límite de registros por página (por defecto 25)
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    empresas_qs = Empresa.objects.all().order_by('nombre')
    paginator = Paginator(empresas_qs, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Preparar opciones de paginación para evitar errores de sintaxis en el template
    per_page_options = []
    for val in [10, 25, 50, 100]:
        per_page_options.append({
            'value': val,
            'selected': per_page == val
        })
    
    return render(request, 'viaticos/empresa_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def empresa_inactivate(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    empresa.activo = not empresa.activo  # Alternar estado
    empresa.actualizadopor = request.user
    empresa.save()
    return redirect('viaticos:empresa_list')

@login_required
def empresa_create(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.creadopor = request.user
            empresa.actualizadopor = request.user
            empresa.save()
            return redirect('viaticos:empresa_list')
    else:
        form = EmpresaForm()
    
    return render(request, 'viaticos/empresa_form.html', {
        'form': form,
        'title': 'Nueva Empresa'
    })

@login_required
def empresa_update(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.actualizadopor = request.user
            empresa.save()
            return redirect('viaticos:empresa_list')
    else:
        form = EmpresaForm(instance=empresa)
    
    return render(request, 'viaticos/empresa_form.html', {
        'form': form,
        'empresa': empresa,
        'title': f'Editar Empresa: {empresa.nombre}'
    })

@login_required
def user_list(request):
    # Obtener el límite de registros por página (por defecto 25)
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    # Obtenemos usuarios con sus perfiles para evitar queries extra (select_related)
    usuarios_qs = User.objects.select_related('perfil', 'perfil__empresa', 'perfil__rol').all().order_by('username')
    paginator = Paginator(usuarios_qs, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Preparar opciones de paginación
    per_page_options = []
    for val in [10, 25, 50, 100]:
        per_page_options.append({
            'value': val,
            'selected': per_page == val
        })
    
    return render(request, 'viaticos/user_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def user_toggle_status(request, pk):
    user_to_toggle = get_object_or_404(User, pk=pk)
    user_to_toggle.is_active = not user_to_toggle.is_active
    user_to_toggle.save()
    
    # También actualizamos la auditoría en el perfil si existe
    profile, created = UserProfile.objects.get_or_create(user=user_to_toggle)
    if created:
        profile.creadopor = request.user
    profile.actualizadopor = request.user
    profile.save()
    
    return redirect('viaticos:user_list')

@login_required
def user_create(request):
    if request.method == 'POST':
        user_form = ExtendedUserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                password = user_form.cleaned_data.get('password')
                if password:
                    user.set_password(password)
                else:
                    # Si no hay password, ponemos uno por defecto para forzar cambio lueg
                    user.set_password('Viajero123*')
                user.save()
                
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.creadopor = request.user
                profile.actualizadopor = request.user
                profile.save()
                
            return redirect('viaticos:user_list')
    else:
        user_form = ExtendedUserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'viaticos/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Nuevo Usuario'
    })

@login_required
def user_update(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    # Asegurar que tenga perfil
    profile_instance, created = UserProfile.objects.get_or_create(user=user_instance)
    
    if request.method == 'POST':
        user_form = ExtendedUserForm(request.POST, instance=user_instance)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile_instance)
        
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                password = user_form.cleaned_data.get('password')
                if password:
                    user.set_password(password)
                user.save()
                profile = profile_form.save(commit=False)
                # Si el perfil se acaba de crear (o no tenía creador), lo asignamos
                if not profile.creadopor:
                    profile.creadopor = request.user
                profile.actualizadopor = request.user
                profile.save()
                
            return redirect('viaticos:user_list')
    else:
        user_form = ExtendedUserForm(instance=user_instance)
        profile_form = UserProfileForm(instance=profile_instance)
        
    return render(request, 'viaticos/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile_instance,
        'title': f'Editar Usuario: {user_instance.username}'
    })

def custom_logout(request):
    if request.method == 'POST' or not request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return redirect('viaticos:home')

@login_required
def role_list(request):
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    roles_qs = Roles.objects.select_related('empresa').all().order_by('empresa__nombre', 'nombre_rol')
    paginator = Paginator(roles_qs, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    per_page_options = [{'value': val, 'selected': per_page == val} for val in [10, 25, 50, 100]]
    
    return render(request, 'viaticos/role_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.creadopor = request.user
            role.actualizadopor = request.user
            role.save()
            return redirect('viaticos:role_list')
    else:
        form = RoleForm()
    
    return render(request, 'viaticos/role_form.html', {
        'form': form,
        'title': 'Nuevo Rol'
    })

@login_required
def role_update(request, pk):
    role = get_object_or_404(Roles, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save(commit=False)
            role.actualizadopor = request.user
            role.save()
            return redirect('viaticos:role_list')
    else:
        form = RoleForm(instance=role)
    
    return render(request, 'viaticos/role_form.html', {
        'form': form,
        'role': role,
        'title': f'Editar Rol: {role.nombre_rol}'
    })

@login_required
def role_toggle_status(request, pk):
    # Por ahora no hay campo 'activo' en Roles, redirigimos simplemente
    return redirect('viaticos:role_list')

@login_required
def tasa_list(request):
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    tasas_qs = TasaCambio.objects.all().order_by('-fecha_valor')
    
    # Filtro por fecha
    q_fecha = request.GET.get('q_fecha')
    if q_fecha:
        tasas_qs = tasas_qs.filter(fecha_valor=q_fecha)

    paginator = Paginator(tasas_qs, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    per_page_options = [{'value': val, 'selected': per_page == val} for val in [10, 25, 50, 100]]
    
    return render(request, 'viaticos/tasa_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'q_fecha': q_fecha,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def tasa_create(request):
    if request.method == 'POST':
        form = TasaCambioForm(request.POST)
        if form.is_valid():
            tasa = form.save(commit=False)
            tasa.creadopor = request.user
            tasa.actualizadopor = request.user
            tasa.save()
            return redirect('viaticos:tasa_list')
    else:
        form = TasaCambioForm()
    
    return render(request, 'viaticos/tasa_form.html', {
        'form': form,
        'title': 'Nueva Tasa de Cambio'
    })

@login_required
def tasa_update(request, pk):
    tasa = get_object_or_404(TasaCambio, pk=pk)
    if request.method == 'POST':
        form = TasaCambioForm(request.POST, instance=tasa)
        if form.is_valid():
            tasa = form.save(commit=False)
            tasa.actualizadopor = request.user
            tasa.save()
            return redirect('viaticos:tasa_list')
    else:
        form = TasaCambioForm(instance=tasa)
    
    return render(request, 'viaticos/tasa_form.html', {
        'form': form,
        'tasa': tasa,
        'title': f'Editar Tasa: {tasa.fecha_valor}'
    })

@login_required
def localidad_list(request):
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    localidades_qs = Localidad.objects.all().order_by('nombre')
    
    # Filtro por nombre o zona
    q = request.GET.get('q')
    if q:
        localidades_qs = localidades_qs.filter(nombre__icontains=q) | localidades_qs.filter(zona__icontains=q)

    paginator = Paginator(localidades_qs, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    per_page_options = [{'value': val, 'selected': per_page == val} for val in [10, 25, 50, 100]]
    
    return render(request, 'viaticos/localidad_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'q': q,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def localidad_create(request):
    if request.method == 'POST':
        form = LocalidadForm(request.POST)
        if form.is_valid():
            localidad = form.save(commit=False)
            localidad.creadopor = request.user
            localidad.actualizadopor = request.user
            localidad.save()
            return redirect('viaticos:localidad_list')
    else:
        form = LocalidadForm()
    
    return render(request, 'viaticos/localidad_form.html', {
        'form': form,
        'title': 'Nueva Localidad'
    })

@login_required
def localidad_update(request, pk):
    localidad = get_object_or_404(Localidad, pk=pk)
    if request.method == 'POST':
        form = LocalidadForm(request.POST, instance=localidad)
        if form.is_valid():
            localidad = form.save(commit=False)
            localidad.actualizadopor = request.user
            localidad.save()
            return redirect('viaticos:localidad_list')
    else:
        form = LocalidadForm(instance=localidad)
    
    return render(request, 'viaticos/localidad_form.html', {
        'form': form,
        'localidad': localidad,
        'title': f'Editar Localidad: {localidad.nombre}'
    })

@login_required
def tipo_viatico_list(request):
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    tipos_qs = TipoViatico.objects.all().order_by('tipo_gasto')
    
    # Filtro por nombre
    q = request.GET.get('q')
    if q:
        tipos_qs = tipos_qs.filter(tipo_gasto__icontains=q)

    paginator = Paginator(tipos_qs, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    per_page_options = [{'value': val, 'selected': per_page == val} for val in [10, 25, 50, 100]]
    
    return render(request, 'viaticos/tipo_viatico_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'q': q,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def tipo_viatico_create(request):
    if request.method == 'POST':
        form = TipoViaticoForm(request.POST)
        if form.is_valid():
            tipo = form.save(commit=False)
            if tipo.gestionadicional:
                tipo.montodolares = 0
            tipo.creadopor = request.user
            tipo.actualizadopor = request.user
            tipo.save()
            return redirect('viaticos:tipo_viatico_list')
    else:
        form = TipoViaticoForm()
    
    return render(request, 'viaticos/tipo_viatico_form.html', {
        'form': form,
        'title': 'Nuevo Tipo de Viático'
    })

@login_required
def tipo_viatico_update(request, pk):
    tipo = get_object_or_404(TipoViatico, pk=pk)
    if request.method == 'POST':
        form = TipoViaticoForm(request.POST, instance=tipo)
        if form.is_valid():
            tipo = form.save(commit=False)
            if tipo.gestionadicional:
                tipo.montodolares = 0
            tipo.actualizadopor = request.user
            tipo.save()
            return redirect('viaticos:tipo_viatico_list')
    else:
        form = TipoViaticoForm(instance=tipo)
    
    return render(request, 'viaticos/tipo_viatico_form.html', {
        'form': form,
        'tipo': tipo,
        'title': f'Editar Tipo de Viático: {tipo.tipo_gasto}'
    })

@login_required
def tipo_viatico_toggle_status(request, pk):
    tipo = get_object_or_404(TipoViatico, pk=pk)
    tipo.activo = not tipo.activo
    tipo.actualizadopor = request.user
    tipo.save()
    return redirect('viaticos:tipo_viatico_list')

from decimal import Decimal

@login_required
def solicitud_list(request):
    per_page = request.GET.get('per_page', 25)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 25

    # Optimizamos con select_related para evitar query N+1
    solicitudes_qs = Solicitud.objects.select_related('solicitante', 'aprobador_administrativo').all().order_by('-nro_solicitud')
    
    # Filtro opcional por solicitante
    q = request.GET.get('q')
    if q:
        solicitudes_qs = solicitudes_qs.filter(solicitante__username__icontains=q) | solicitudes_qs.filter(solicitante__first_name__icontains=q)

    paginator = Paginator(solicitudes_qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    per_page_options = [{'value': val, 'selected': per_page == val} for val in [10, 25, 50, 100]]
    
    return render(request, 'viaticos/solicitud_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'q': q,
        'pagination': {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current': page_obj.number,
            'total': page_obj.paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
        }
    })

@login_required
def solicitud_create(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        formset = SolicitudDetalleFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                solicitud = form.save(commit=False)
                
                # Regla: El aprobador es el supervisor del solicitante
                try:
                    perfil_solicitante = solicitud.solicitante.perfil
                    if perfil_solicitante.supervisor:
                        solicitud.aprobador_administrativo = perfil_solicitante.supervisor.user
                except UserProfile.DoesNotExist:
                    pass
                
                solicitud.creadopor = request.user
                solicitud.actualizadopor = request.user
                solicitud.save()
                
                # Guardar detalles y calcular total dólares
                formset.instance = solicitud
                detalles = formset.save(commit=False)
                total_usd = Decimal('0.00')
                
                for detalle in detalles:
                    # Regla: Monto = cantidad * monto_tipo (solo si no es gestionadicional)
                    if not detalle.tipo_viatico.gestionadicional:
                        detalle.monto_dolares = Decimal(detalle.cantidad) * detalle.tipo_viatico.montodolares
                    else:
                        detalle.monto_dolares = Decimal('0.00')
                    
                    detalle.save()
                    total_usd += detalle.monto_dolares
                
                # También sumar los que no cambiaron (por si es un update, aunque este es create)
                # En create, solo sumamos lo nuevo.
                
                solicitud.total_dolares = total_usd
                
                # Calcular Bolívares según tasa del día
                tasa = TasaCambio.objects.filter(fecha_valor=solicitud.fecha_solicitud).first()
                if tasa:
                    solicitud.total_bolivares = solicitud.total_dolares * tasa.tasa_dolar
                else:
                    solicitud.total_bolivares = Decimal('0.00')
                
                solicitud.save()
                
            return redirect('viaticos:solicitud_list')
    else:
        form = SolicitudForm(initial={'solicitante': request.user, 'empresa': request.user.perfil.empresa})
        # Inicializar cantidad_personas si se desea
        formset = SolicitudDetalleFormSet()
        
    return render(request, 'viaticos/solicitud_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Nueva Solicitud de Viáticos'
    })

@login_required
def solicitud_update(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        formset = SolicitudDetalleFormSet(request.POST, instance=solicitud)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                solicitud = form.save(commit=False)
                
                # Recalcular aprobador si cambió el solicitante
                try:
                    perfil_solicitante = solicitud.solicitante.perfil
                    if perfil_solicitante.supervisor:
                        solicitud.aprobador_administrativo = perfil_solicitante.supervisor.user
                except UserProfile.DoesNotExist:
                    pass
                
                solicitud.actualizadopor = request.user
                solicitud.save()
                
                # Procesar detalles
                instancias = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                
                for detalle in instancias:
                    if not detalle.tipo_viatico.gestionadicional:
                        detalle.monto_dolares = Decimal(detalle.cantidad) * detalle.tipo_viatico.montodolares
                    else:
                        detalle.monto_dolares = Decimal('0.00')
                    detalle.save()
                
                # Recalcular totales
                total_usd = solicitud.detalles.aggregate(total=Sum('monto_dolares'))['total'] or Decimal('0.00')
                solicitud.total_dolares = total_usd
                
                tasa = TasaCambio.objects.filter(fecha_valor=solicitud.fecha_solicitud).first()
                if tasa:
                    solicitud.total_bolivares = solicitud.total_dolares * tasa.tasa_dolar
                else:
                    solicitud.total_bolivares = Decimal('0.00')
                
                solicitud.save()
                
            return redirect('viaticos:solicitud_list')
    else:
        form = SolicitudForm(instance=solicitud)
        formset = SolicitudDetalleFormSet(instance=solicitud)
    
    return render(request, 'viaticos/solicitud_form.html', {
        'form': form,
        'formset': formset,
        'solicitud': solicitud,
        'title': f'Editar Solicitud #{solicitud.nro_solicitud}'
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room
from .forms import RoomForm

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user.profile
            room.save()
            form.save_m2m()
            
            # Si es sala privada, mostrar el código
            if room.privacy == 'privada':
                return redirect('rooms:room_created', room_id=room.id)
            else:
                # Si es pública, ir directo a Jitsi
                return redirect(room.url_jitsi)
    else:
        form = RoomForm()
    
    return render(request, 'rooms/create_room.html', {'form': form})

@login_required
def access_room(request):
    """Vista para acceder a una sala mediante código"""
    if request.method == 'POST':
        code = request.POST.get('access_code', '').strip().upper()
        
        if not code:
            messages.error(request, 'Por favor ingresa un código de acceso.')
            return render(request, 'rooms/access_room.html')
        
        try:
            # Buscar sala por código
            room = Room.objects.get(access_code=code, active=True)
            
            # Verificar que sea sala privada
            if room.privacy != 'privada':
                messages.error(request, 'Este código no es válido.')
                return render(request, 'rooms/access_room.html')
            
            # Redirigir a la URL de Jitsi
            return redirect(room.url_jitsi)
            
        except Room.DoesNotExist:
            messages.error(request, 'Código de acceso inválido o sala inactiva.')
            return render(request, 'rooms/access_room.html')
    
    return render(request, 'rooms/access_room.html')

# NUEVA VISTA - Mostrar código después de crear sala privada
@login_required
def room_created(request, room_id):
    """Muestra el código de acceso de una sala recién creada"""
    room = get_object_or_404(Room, id=room_id, creator=request.user.profile)
    return render(request, 'rooms/room_created.html', {'room': room})
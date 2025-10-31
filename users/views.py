from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileEditForm
from django.templatetags.static import static

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            print(form.errors)

            print("Se creo el usuario")
            
            # El perfil ya existe gracias a la señal
            profile = user.profile
            profile.bio = form.cleaned_data.get('bio')
            profile.profile_picture = form.cleaned_data.get('profile_picture')
            instruments_data = form.cleaned_data.get('instruments') or []
            if hasattr(profile, 'instruments'):
                profile.instruments.set(instruments_data)
            profile.save()
            return redirect('users:login')
    else:
        print("error")
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Verifica si el usuario existe y la contraseña es correcta
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Crea la sesión
            return redirect("pages:feed")  # Redirige a tu página principal
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")

    return render(request, "users/login.html")  # Renderiza tu template del login


def logout_view(request):
    logout(request)
    return redirect("users:login")

@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=request.user.username)  # ajusta a tu nombre de ruta
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, "users/profile_edit.html", {"form": form, "profile": profile})



def _extract_playlist_id(url: str) -> str | None:
    if not url:
        return None
    try:
        if "open.spotify.com/playlist/" in url:
            part = url.split("open.spotify.com/playlist/")[1]
            return part.split("?")[0].strip("/")
        if url.startswith("spotify:playlist:"):
            return url.split(":")[-1]
    except Exception:
        return None
    return None

@login_required
def profile_view(request, username=None):
    # usuario objetivo
    user_obj = get_object_or_404(User, username=username) if username else request.user
    profile = getattr(user_obj, "profile", None)

    # --- Avatar seguro ---
    # Usa 'avatar' si tu modelo lo llama así; si tu campo se llama 'profile_picture', cambia a ese nombre.
    avatar_url = static('images/default_avatar.png')
    if profile and getattr(profile, "profile_picture", None):
        try:
            if profile.profile_picture and profile.profile_picture.url:
                avatar_url = profile.profile_picture.url
        except Exception:
            pass  # si falla, deja el default

    # --- Header: soporta texto O imagen (según tu modelo real) ---
    # Definir por defecto para evitar NameError y calcular independientemente
    header_image_url = ""
    try:
        if profile and getattr(profile, "header", None):
            # Si el campo header es un FileField/ImageField tendrá .url
            if getattr(profile.header, 'url', None):
                header_image_url = profile.header.url
            else:
                # Si header es texto (string), dejamos header_image_url vacío
                header_image_url = ""
    except Exception:
        # Si algo falla, dejamos el header vacío y seguimos
        header_image_url = ""

    # --- Spotify ---
    playlist_id = ""
    spotify_url = getattr(profile, "spotify_playlist_url", "") if profile else ""
    if spotify_url:
        playlist_id = _extract_playlist_id(spotify_url) or ""
    has_playlist = bool(playlist_id)
    spotify_embed_src = f"https://open.spotify.com/embed/playlist/{playlist_id}" if has_playlist else ""

    ctx = {
        "profile": profile,
        "is_owner": request.user == user_obj,
        "avatar_url": avatar_url,
        "header_image_url": header_image_url,
        "has_playlist": has_playlist,
        "spotify_embed_src": spotify_embed_src,
    }
    return render(request, "users/profile.html", ctx)
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from instruments.models import Instrument
from users.models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )
    instruments = forms.ModelMultipleChoiceField(
        queryset=Instrument.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "inp-cbx"}),
        required=False
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'instruments', 'profile_picture']

    def save(self, commit=True):
        """Save the User and populate the related Profile with extra fields.

        This ensures that 'bio', 'profile_picture' and 'instruments' provided
        at registration are stored on the Profile immediately.
        """
        user = super().save(commit=commit)

        # Ensure profile exists (signal usually creates it, but be defensive)
        try:
            profile = user.profile
        except Exception:
            profile = Profile.objects.create(user=user)

        # Populate profile fields from the form cleaned_data
        bio = self.cleaned_data.get('bio')
        if bio is not None:
            profile.bio = bio

        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            profile.profile_picture = profile_picture

        instruments_data = self.cleaned_data.get('instruments') or []
        profile.save()
        if hasattr(profile, 'instruments'):
            profile.instruments.set(instruments_data)

        return user



class ProfileEditForm(forms.ModelForm):
    """Formulario para editar el perfil del usuario"""
    
    class Meta:
        model = Profile
        fields = ['profile_picture', 'header', 'bio', 'instruments', 'spotify_playlist_url']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos sobre ti, tu experiencia musical, géneros favoritos...'
            }),
            'instruments': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'header': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'spotify_playlist_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://open.spotify.com/playlist/...'
            })
        }
        labels = {
            'profile_picture': 'Foto de Perfil',
            'header': 'Imagen de Cabecera',
            'bio': 'Biografía',
            'instruments': 'Instrumentos que tocas',
            'spotify_playlist_url': 'Playlist de Spotify (opcional)'
        }
        help_texts = {
            'spotify_playlist_url': 'Copia y pega el enlace de tu playlist pública de Spotify',
            'header': 'Imagen que aparecerá en la parte superior de tu perfil (recomendado: 1200x300px)',
            'profile_picture': 'Tu foto de perfil (se mostrará circular)'
        }
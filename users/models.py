from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from instruments.models import Instrument
from django.core.validators import RegexValidator, URLValidator
from django.utils.text import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    header = models.ImageField(upload_to='headers/', blank=True, null=True)  
    spotify_playlist_url = models.URLField(blank=True, validators=[URLValidator()])
    instruments = models.ManyToManyField(Instrument, blank=True, related_name="musicians")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    playlist_id = models.CharField(
        max_length=64, blank=True,
        validators=[RegexValidator(regex=r"^[A-Za-z0-9]+$", message="ID de playlist inválido.", code="invalid_id")]
    )
    


def __str__(self):
        return f"Perfil de {self.user}"

def save(self, *args, **kwargs):
        # Si nos dieron la URL de la playlist y no hay ID, intenta extraerlo
        if self.spotify_playlist_url and not self.playlist_id:
            self.playlist_id = self._extract_playlist_id(self.spotify_playlist_url) or self.playlist_id
        super().save(*args, **kwargs)

@staticmethod
def _extract_playlist_id(url: str):
        """
        Acepta:
          - https://open.spotify.com/playlist/{id}
          - https://open.spotify.com/playlist/{id}?si=...
          - spotify:playlist:{id}
        """
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

@property
def spotify_embed_src(self):
        """
        Devuelve la URL para el iframe embed si hay playlist.
        """
        pid = self.playlist_id or self._extract_playlist_id(self.spotify_playlist_url or "")
        if pid:
            return f"https://open.spotify.com/embed/playlist/{pid}"
        return ""



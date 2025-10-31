from django.db import models
import secrets
from instruments.models import Instrument
from users import models as users


class Room(models.Model):
    PRIVACY_OPTIONS = [
        ('publica', 'Pública'),
        ('privada', 'Privada'),
    ]

    room_name = models.CharField(max_length=100)
    room_description = models.TextField(blank=True)
    creator = models.ForeignKey(users.Profile, on_delete=models.CASCADE)
    required_instruments = models.ManyToManyField(Instrument, blank=True)
    privacy = models.CharField(max_length=20, choices=[('publica', 'Pública'), ('privada', 'Privada')])
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    url_jitsi = models.URLField(blank=True)
    access_code = models.CharField(max_length=12, unique=True, blank=True)

    def generate_access_code(self):
        """Genera un código aleatorio de 8 caracteres alfanuméricos"""
        return secrets.token_urlsafe(6)[:8].upper()
    
    def save(self, *args, **kwargs):
        # Si es sala privada y no tiene código, generarlo
        if self.privacy == 'privada' and not self.access_code:
            self.access_code = self.generate_access_code()
            # Asegurar que el código sea único
            while Room.objects.filter(access_code=self.access_code).exists():
                self.access_code = self.generate_access_code()
        
        # Si es sala pública, limpiar el código
        if self.privacy == 'publica':
            self.access_code = ''
        
        # Generar URL de Jitsi si no existe
        if not self.url_jitsi:
            self.url_jitsi = f"https://meet.jit.si/{self.room_name.replace(' ', '_')}"
        
        super().save(*args, **kwargs)
from django.db import models
import secrets
from instruments.models import Instrument
from users import models as users
from django.db import transaction, IntegrityError 


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
    access_code = models.CharField(unique=True, null=True, blank=True)

    def generate_access_code(self):
        """Genera un código aleatorio de 8 caracteres alfanuméricos"""
        return secrets.token_urlsafe(6)[:8].upper()
    

    def save(self, *args, **kwargs):
        # 1) Limpiar/generar access_code según privacidad
        if self.privacy == 'publica':
            # MUY IMPORTANTE: usar None (NULL), no cadena vacía
            self.access_code = None
        else:  # 'privada'
            if not self.access_code:  # si no viene, generarlo
                for _ in range(20):  # reintentos contra colisiones
                    self.access_code = self.generate_access_code()
                    try:
                        with transaction.atomic():
                            # 2) Completar otros campos antes de guardar
                            if not self.url_jitsi:
                                self.url_jitsi = f"https://meet.jit.si/{self.room_name.replace(' ', '_')}"
                            return super().save(*args, **kwargs)
                    except IntegrityError:
                        # choque de UNIQUE en access_code → intenta otro
                        continue
                # si no se logró tras varios intentos
                raise RuntimeError("No se pudo generar un access_code único tras varios intentos.")

        # 2) Completar otros campos (para pública o privada con code ya dado)
        if not self.url_jitsi:
            self.url_jitsi = f"https://meet.jit.si/{self.room_name.replace(' ', '_')}"

        # 3) Guardado normal
        return super().save(*args, **kwargs)
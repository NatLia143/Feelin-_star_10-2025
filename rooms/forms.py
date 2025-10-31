from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'room_description', 'required_instruments', 'privacy']
        widgets = {
            'required_instruments': forms.CheckboxSelectMultiple,  # Selección múltiple de instrumentos
        }
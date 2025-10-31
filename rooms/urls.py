from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("crear/", views.create_room, name="create_room"),
    path('acceder/', views.access_room, name='access_room'),  
    path('creada/<int:room_id>/', views.room_created, name='room_created'), 
]
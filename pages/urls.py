from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('privacy/', views.privacy, name='privacy'),  # Política de privacidad
    path('terms/', views.terms, name='terms'), # Términos y condiciones
    path('about/', views.about, name='about'),  # Página "Acerca de"
    path('feed/', views.feed, name='feed'),  # Página de feed
]
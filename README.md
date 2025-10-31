# Feelin' Star

 Feelin' Star es una plataforma para músicos que permite crear y gestionar salas virtuales de ensayo, así como manejar perfiles de usuario.

## Funcionalidades actuales

- Registro de usuarios con perfil personalizado.
- Inicio y cierre de sesión.
- Redirección automática tras registro y login.
- Creación de salas (solo usuarios autenticados).
- Gestión automática de perfiles de usuario.

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL-del-repositorio>
   ```
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Realiza las migraciones:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Ejecuta el servidor:
   ```
   python manage.py runserver
   ```

## Estructura principal

- `users/` - Registro, login, logout y perfiles.
- `rooms/` - Creación de salas.
- `pages/` - Páginas informativas.
- `static/` y `templates/` - Archivos estáticos y plantillas.

## Estado actual

El proyecto permite registrar usuarios, iniciar/cerrar sesión y crear salas. La gestión de perfiles es automática.  
Faltan funcionalidades avanzadas.

---

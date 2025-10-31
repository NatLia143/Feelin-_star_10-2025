from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

app_name = "users"

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pages:index'), name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),    
]

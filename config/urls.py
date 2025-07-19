from django.contrib import admin
from django.urls import path
from app.views import (
    IndexView,
    CustomLoginView as LoginView,
    CustomLogoutView as LogoutView,
    RegistroView,
    PerfilView,
    UsuariosView,
    LivrosView,
    DetalhesLivroView,
    DesafiosView,
    RecompensasView,
    RankingView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Usuários
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    
    # Livros
    path('livros/', LivrosView.as_view(), name='livros'),
    path('livros/<int:pk>/', DetalhesLivroView.as_view(), name='detalhes_livro'),
    
    # Gamificação
    path('desafios/', DesafiosView.as_view(), name='desafios'),
    path('recompensas/', RecompensasView.as_view(), name='recompensas'),
    path('ranking/', RankingView.as_view(), name='ranking'),
]
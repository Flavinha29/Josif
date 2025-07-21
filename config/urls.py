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
    RecomendacoesView,
    DesafiosView,
    AvaliacoesView,
    RankingView,
    ProgressoView,
    ConquistasView
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
    path('recomendacoes/', RecomendacoesView.as_view(), name='recomendacoes'),
    path('desafios/', DesafiosView.as_view(), name='desafios'),
    path('avaliacoes/', AvaliacoesView.as_view(), name='avaliacoes'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('progresso/', ProgressoView.as_view(), name='progresso'),
    path('conquistas/', ConquistasView.as_view(), name='conquistas'),
]
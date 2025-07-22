from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Pessoa, Livro, DesafioLeitura, Recompensa, RankingLeitura, ProgressoLeitura

# Views básicas
class IndexView(TemplateView):
    template_name = 'app/index.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/'

class RegistroView(CreateView):
    template_name = 'registration/registro.html'
    success_url = '/login/'

# Views para perfil e usuários
class PerfilView(LoginRequiredMixin, DetailView):
    model = Pessoa
    template_name = 'registration/perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user

class UsuariosView(LoginRequiredMixin, ListView):
    model = Pessoa
    template_name = 'registration/usuarios.html'
    context_object_name = 'usuarios'

# Views para livros
class LivrosView(ListView):
    model = Livro
    template_name = 'app/livros.html'
    context_object_name = 'livros'

class DetalhesLivroView(DetailView):
    model = Livro
    template_name = 'app/detalhes_livro.html'
    context_object_name = 'livro'

# Views para gamificação
class RecomendacoesView(LoginRequiredMixin, ListView):
    template_name = 'app/recomendacoes.html'
    context_object_name = 'livros'
    
    def get_queryset(self):
        # Garanta que retorna algum resultado
        return Livro.objects.all()[:6]  # Exemplo simples
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['livros']:
            context['mensagem'] = "Nenhuma recomendação encontrada"
        return context

class DesafiosView(LoginRequiredMixin, ListView):
    model = DesafioLeitura
    template_name = 'app/desafios.html'
    context_object_name = 'desafios'

    def get_queryset(self):
        return DesafioLeitura.objects.filter(ativo=True)

class AvaliacoesView(LoginRequiredMixin, ListView):
    template_name = 'app/avaliacoes.html'
    context_object_name = 'avaliacoes'

    def get_queryset(self):
        # Lógica para retornar avaliações do usuário
        return []

class RankingView(ListView):
    template_name = 'app/ranking.html'
    context_object_name = 'ranking'

    def get_queryset(self):
        # Lógica para retornar o ranking ordenado por pontos
        return Pessoa.objects.order_by('-pontos_leitura')[:10]

class ProgressoView(LoginRequiredMixin, ListView):
    template_name = 'app/progresso.html'
    context_object_name = 'progressos'

    def get_queryset(self):
        return ProgressoLeitura.objects.filter(estudante=self.request.user)

class ConquistasView(LoginRequiredMixin, ListView):
    model = Recompensa
    template_name = 'app/conquistas.html'
    context_object_name = 'recompensas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conquistas_aluno'] = []  # Adicionar lógica para conquistas do aluno
        return context
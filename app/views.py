from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pessoa, Livro, DesafioLeitura, Recompensa

# Views básicas
class IndexView(TemplateView):
    template_name = 'index.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/'

class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registro.html'
    success_url = '/login/'

# Views para perfil e usuários
class PerfilView(LoginRequiredMixin, DetailView):
    model = Pessoa
    template_name = 'perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user

class UsuariosView(LoginRequiredMixin, ListView):
    model = Pessoa
    template_name = 'usuarios.html'
    context_object_name = 'usuarios'

# Views para livros
class LivrosView(ListView):
    model = Livro
    template_name = 'livros.html'
    context_object_name = 'livros'

class DetalhesLivroView(DetailView):
    model = Livro
    template_name = 'detalhes_livro.html'
    context_object_name = 'livro'

# Views para desafios e recompensas
class DesafiosView(ListView):
    model = DesafioLeitura
    template_name = 'desafios.html'
    context_object_name = 'desafios'

class RecompensasView(ListView):
    model = Recompensa
    template_name = 'recompensas.html'
    context_object_name = 'recompensas'

class RankingView(ListView):
    template_name = 'ranking.html'
    context_object_name = 'ranking'
    
    def get_queryset(self):
        # Lógica para retornar o ranking ordenado por pontos
        return Pessoa.objects.order_by('-pontos_leitura')[:10]
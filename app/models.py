from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Pessoa(AbstractUser):
    """Modelo extendido de usuário para o sistema"""
    data_nascimento = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    pontos_leitura = models.IntegerField(default=0, verbose_name="Pontos acumulados")
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True, verbose_name="Foto de perfil")
    
    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

class GeneroLiterario(models.Model):
    """Gêneros de livros disponíveis no sistema"""
    nome = models.CharField(max_length=50, verbose_name="Gênero Literário")
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Gênero Literário"
        verbose_name_plural = "Gêneros Literários"

class Livro(models.Model):
    """Livros disponíveis na plataforma"""
    titulo = models.CharField(max_length=200, verbose_name="Título")
    autor = models.CharField(max_length=100, verbose_name="Autor")
    genero = models.ForeignKey(GeneroLiterario, on_delete=models.SET_NULL, null=True, verbose_name="Gênero")
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    capa = models.ImageField(upload_to='capas/', null=True, blank=True, verbose_name="Capa do Livro")
    paginas = models.IntegerField(verbose_name="Número de páginas", default=0)
    faixa_etaria = models.CharField(max_length=20, verbose_name="Faixa etária recomendada", default="Livre")
    
    def __str__(self):
        return f"{self.titulo} ({self.autor})"

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

class DesafioLeitura(models.Model):
    """Desafios de leitura para os usuários"""
    titulo = models.CharField(max_length=200, verbose_name="Título do Desafio")
    descricao = models.TextField(verbose_name="Descrição")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de término")
    ativo = models.BooleanField(default=True, verbose_name="Desafio ativo")
    livros = models.ManyToManyField(Livro, verbose_name="Livros do desafio")
    
    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Desafio de Leitura"
        verbose_name_plural = "Desafios de Leitura"

class Recompensa(models.Model):
    """Recompensas por conquistas na plataforma"""
    nome = models.CharField(max_length=100, verbose_name="Nome da Recompensa")
    descricao = models.TextField(verbose_name="Descrição")
    pontos_necessarios = models.IntegerField(verbose_name="Pontos necessários")
    imagem = models.ImageField(upload_to='recompensas/', null=True, blank=True, verbose_name="Ícone da Recompensa")
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"

class ProgressoLeitura(models.Model):
    """Progresso dos usuários na leitura dos livros"""
    STATUS = [
        ('L', 'Lendo'),
        ('C', 'Concluído'),
    ]
    
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Estudante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    status = models.CharField(max_length=1, choices=STATUS, default='L', verbose_name="Status")
    data_inicio = models.DateField(auto_now_add=True, verbose_name="Data de início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de conclusão")
    progresso_paginas = models.IntegerField(default=0, verbose_name="Páginas lidas")
    
    def __str__(self):
        return f"{self.estudante} - {self.livro} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Progresso de Leitura"
        verbose_name_plural = "Progressos de Leitura"

class RankingLeitura(models.Model):
    """Ranking de leitura dos usuários"""
    PERIODO = [
        ('M', 'Mensal'),
        ('A', 'Anual'),
    ]
    
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Estudante")
    pontos_totais = models.IntegerField(default=0, verbose_name="Pontos totais")
    periodo = models.CharField(max_length=1, choices=PERIODO, verbose_name="Período")
    data_registro = models.DateField(auto_now_add=True, verbose_name="Data do registro")
    
    def __str__(self):
        return f"{self.estudante} - {self.pontos_totais} pontos ({self.get_periodo_display()})"

    class Meta:
        verbose_name = "Ranking de Leitura"
        verbose_name_plural = "Rankings de Leitura"

class Avaliacao(models.Model):
    """Avaliações dos usuários sobre os livros"""
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    usuario = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Usuário")
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota (1-5)"
    )
    comentario = models.TextField(blank=True, verbose_name="Comentário")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da avaliação")
    
    def __str__(self):
        return f"Avaliação de {self.usuario} para {self.livro}"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ('livro', 'usuario')
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Cidade(models.Model):
    """RF06 - Gerenciar cidades"""
    nome = models.CharField(max_length=100, verbose_name="Nome da cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")

    def __str__(self):
        return f"{self.nome}, {self.uf}"

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

class Ocupacao(models.Model):
    """RF02 - Gerenciar ocupação"""
    nome = models.CharField(max_length=50, verbose_name="Ocupação")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Ocupação"
        verbose_name_plural = "Ocupações"

class Escola(models.Model):
    """RF03 - Gerenciar escolas"""
    nome = models.CharField(max_length=100, verbose_name="Nome da escola")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, verbose_name="Cidade")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"

class Pessoa(AbstractUser):
    """RF01 - Gerenciar pessoas (usuários do sistema)"""
    data_nascimento = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    ocupacao = models.ForeignKey(Ocupacao, on_delete=models.SET_NULL, null=True, verbose_name="Ocupação")
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Escola")
    pontos_leitura = models.IntegerField(default=0, verbose_name="Pontos acumulados")
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True, verbose_name="Foto de perfil")

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

class Turma(models.Model):
    """RF04 - Gerenciar turmas"""
    TURNOS = [
        ('M', 'Matutino'),
        ('V', 'Vespertino'),
    ]

    nome = models.CharField(max_length=50, verbose_name="Nome da turma")
    ano_escolar = models.CharField(max_length=10, verbose_name="Ano escolar (6º ao 9º)")
    turno = models.CharField(max_length=1, choices=TURNOS, verbose_name="Turno")
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, verbose_name="Escola")
    professor_responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, limit_choices_to={'ocupacao__nome': 'Professor'}, verbose_name="Professor Responsável")

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

class GeneroLiterario(models.Model):
    """RF07 - Gerenciar gêneros literários"""
    nome = models.CharField(max_length=50, verbose_name="Gênero Literário")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Gênero Literário"
        verbose_name_plural = "Gêneros Literários"

class Livro(models.Model):
    """RF05 - Gerenciar livros"""
    titulo = models.CharField(max_length=200, verbose_name="Título")
    autor = models.CharField(max_length=100, verbose_name="Autor")
    genero = models.ForeignKey(GeneroLiterario, on_delete=models.SET_NULL, null=True, verbose_name="Gênero")
    faixa_etaria = models.CharField(max_length=20, verbose_name="Faixa etária")
    paginas = models.IntegerField(verbose_name="Número de páginas")
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    capa = models.ImageField(upload_to='capas/', null=True, blank=True, verbose_name="Capa do Livro")

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

class Emprestimo(models.Model):
    """RF09 - Gerenciar empréstimos de livros"""
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'ocupacao__nome': 'Estudante'}, verbose_name="Estudante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    data_emprestimo = models.DateField(auto_now_add=True, verbose_name="Data do empréstimo")
    data_devolucao = models.DateField(null=True, blank=True, verbose_name="Data de devolução")

    def __str__(self):
        return f"{self.estudante} - {self.livro}"

    class Meta:
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"

class AvaliacaoLeitura(models.Model):
    """RF08 - Gerenciar avaliações de leitura"""
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'ocupacao__nome': 'Estudante'}, verbose_name="Estudante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota"
    )
    feedback = models.TextField(blank=True, verbose_name="Feedback")

    def __str__(self):
        return f"Avaliação de {self.estudante} para {self.livro}"

    class Meta:
        verbose_name = "Avaliação de Leitura"
        verbose_name_plural = "Avaliações de Leitura"

class DesafioLeitura(models.Model):
    """RF12 - Gerenciar desafios de leitura"""
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de término")
    livros = models.ManyToManyField(Livro, verbose_name="Livros do desafio")
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Turma")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Desafio de Leitura"
        verbose_name_plural = "Desafios de Leitura"

class Recompensa(models.Model):
    """RF11 - Gerenciar recompensas"""
    nome = models.CharField(max_length=100, verbose_name="Nome da Recompensa")
    descricao = models.TextField(verbose_name="Descrição")
    pontos_necessarios = models.IntegerField(verbose_name="Pontos necessários")
    imagem = models.ImageField(upload_to='recompensas/', null=True, blank=True, verbose_name="Imagem")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"

class RankingLeitura(models.Model):
    """RF10 - Gerenciar ranking de leitura"""
    PERIODO = [
        ('M', 'Mensal'),
        ('A', 'Anual'),
    ]

    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Turma")
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'ocupacao__nome': 'Estudante'}, verbose_name="Estudante")
    pontos_totais = models.IntegerField(verbose_name="Pontos totais")
    periodo = models.CharField(max_length=1, choices=PERIODO, verbose_name="Período")

    def __str__(self):
        return f"{self.estudante} - {self.pontos_totais} pontos"

    class Meta:
        verbose_name = "Ranking de Leitura"
        verbose_name_plural = "Rankings de Leitura"

class RelatorioDesempenho(models.Model):
    """RF13 - Gerar e analisar relatórios"""
    professor = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'ocupacao__nome': 'Professor'}, verbose_name="Professor")
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='relatorios', limit_choices_to={'ocupacao__nome': 'Estudante'}, verbose_name="Estudante")
    desempenho = models.TextField(verbose_name="Desempenho")
    recomendacoes = models.TextField(verbose_name="Recomendações")
    data_criacao = models.DateField(auto_now_add=True, verbose_name="Data do relatório")

    def __str__(self):
        return f"Relatório de {self.estudante}"

    class Meta:
        verbose_name = "Relatório de Desempenho"
        verbose_name_plural = "Relatórios de Desempenho"

class RecomendacaoLeitura(models.Model):
    """RF14 - Gerenciar recomendações de leitura"""
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'ocupacao__nome': 'Estudante'}, verbose_name="Estudante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    criterio = models.CharField(max_length=100, verbose_name="Critério de recomendação")
    data_recomendacao = models.DateField(auto_now_add=True, verbose_name="Data da recomendação")

    def __str__(self):
        return f"Recomendação para {self.estudante}"

    class Meta:
        verbose_name = "Recomendação de Leitura"
        verbose_name_plural = "Recomendações de Leitura"

class ProgressoLeitura(models.Model):
    """RF15 - Gerenciar progresso de leitura"""
    STATUS = [
        ('L', 'Lendo'),
        ('C', 'Concluído'),
    ]

    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, limit_choices_to={'ocupacao__nome': 'Estudante'}, verbose_name="Estudante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    status = models.CharField(max_length=1, choices=STATUS, verbose_name="Status")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Data de conclusão")

    def __str__(self):
        return f"{self.estudante} - {self.livro} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Progresso de Leitura"
        verbose_name_plural = "Progressos de Leitura"
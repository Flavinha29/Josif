from django.db import models
from django.contrib.auth.models import AbstractUser

# RF06: Gerenciar cidades
class Cidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")

    def __str__(self):
        return f"{self.nome}, {self.uf}"

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

# RF02: Gerenciar ocupação (professor/estudante)
class Ocupacao(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Ocupação (ex: Professor, Estudante)")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Ocupação"
        verbose_name_plural = "Ocupações"

# RF03: Gerenciar escolas
class Escola(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da escola")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"

# RF04: Gerenciar turmas
class Turma(models.Model):
    TURNOS = [
        ('M', 'Matutino'),
        ('V', 'Vespertino'),
    ]

    nome = models.CharField(max_length=50, verbose_name="Nome da turma")
    ano_escolar = models.CharField(max_length=10, verbose_name="Ano escolar (6º ao 9º)")
    turno = models.CharField(max_length=1, choices=TURNOS, verbose_name="Turno")
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, verbose_name="Escola")

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

# RF01: Gerenciar pessoas (usuários do sistema)
class Pessoa(AbstractUser):
    data_nascimento = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    ocupacao = models.ForeignKey(Ocupacao, on_delete=models.SET_NULL, null=True, verbose_name="Ocupação")
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Escola")
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Turma")
    pontos_leitura = models.IntegerField(default=0, verbose_name="Pontos acumulados")

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

# RF07: Gerenciar gêneros literários
class GeneroLiterario(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Gênero (ex: Aventura, Mistério)")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Gênero Literário"
        verbose_name_plural = "Gêneros Literários"

# RF05: Gerenciar livros
class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    autor = models.CharField(max_length=100, verbose_name="Autor")
    genero = models.ForeignKey(GeneroLiterario, on_delete=models.SET_NULL, null=True, verbose_name="Gênero")
    faixa_etaria = models.CharField(max_length=20, verbose_name="Faixa etária")
    paginas = models.IntegerField(verbose_name="Número de páginas")
    descricao = models.TextField(verbose_name="Descrição", blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

# RF15: Gerenciar progresso de leitura
class ProgressoLeitura(models.Model):
    STATUS = [
        ('L', 'Lendo'),
        ('C', 'Concluído'),
    ]

    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Estudante")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    status = models.CharField(max_length=1, choices=STATUS, verbose_name="Status")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de conclusão", null=True, blank=True)

    def __str__(self):
        return f"{self.estudante} - {self.livro} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Progresso de Leitura"
        verbose_name_plural = "Progressos de Leitura"

# RF11: Gerenciar recompensas
class Recompensa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da recompensa")
    descricao = models.TextField(verbose_name="Descrição")
    pontos_necessarios = models.IntegerField(verbose_name="Pontos necessários")
    imagem = models.ImageField(upload_to='recompensas/', verbose_name="Imagem", null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"

# RF12: Gerenciar desafios de leitura
class DesafioLeitura(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de término")
    livros = models.ManyToManyField(Livro, verbose_name="Livros do desafio")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Desafio de Leitura"
        verbose_name_plural = "Desafios de Leitura"

# RF10: Gerenciar ranking de leitura
class RankingLeitura(models.Model):
    PERIODO = [
        ('M', 'Mensal'),
        ('A', 'Anual'),
    ]

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    estudante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Estudante")
    pontos_totais = models.IntegerField(verbose_name="Pontos totais")
    periodo = models.CharField(max_length=1, choices=PERIODO, verbose_name="Período")

    def __str__(self):
        return f"{self.estudante} - {self.get_periodo_display()}"

    class Meta:
        verbose_name = "Ranking de Leitura"
        verbose_name_plural = "Rankings de Leitura"
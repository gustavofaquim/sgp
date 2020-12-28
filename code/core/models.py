from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Disciplina(models.Model):
    disciplina = models.CharField(max_length=250)

    def __str__(self):
        return str(self.disciplina)

    class Meta:
        db_table = "disciplina"

class Categoria(models.Model):
    categoria = models.CharField(max_length=400)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.categoria)

    class Meta:
        db_table = "categoria"

class SubCategoria(models.Model):
    subcategoria = models.CharField(max_length=400)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.subcategoria)

    class Meta:
        db_table = "subcategoria"

class Origem(models.Model):
    origem = models.CharField(max_length=250)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return str(self.origem)

    class Meta:
        db_table = "origem"


class Professor(models.Model):
    user = models.ForeignKey(User, related_name='professor', unique=True, on_delete=models.CASCADE)
    cpf = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=350)
    email = models.EmailField()
    nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    foto = models.ImageField(upload_to="professor/", null=True, blank=True)
    disciplina = models.ManyToManyField(Disciplina, null=False, blank=False, related_name='disciplinas')

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = "professor"
        verbose_name_plural = "Professores"

    

class Tag(models.Model):
    tag = models.CharField(max_length=30)

    def __str__(self):
        return str(self.tag)

    class Meta:
        db_table = "tag"
        verbose_name_plural = "Tags"


class Questao(models.Model):
    nome = models.CharField(max_length=300)
    enunciado = RichTextUploadingField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, blank=True, null=True)
    origem = models.ForeignKey(Origem, on_delete=models.CASCADE, blank=True, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = "questao"
        verbose_name_plural = "Questões"

class Alternativa(models.Model):
    alternativa = models.TextField()
    correta = models.BooleanField(default=False,null=False, blank=False)
    imagem = models.ImageField(upload_to="alternativa/", null=True, blank=True)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')
    letra = models.CharField(max_length=1)

    def __str__(self):
        return str(self.alternativa)

    class Meta:
        db_table = "alternativa"

class Cabecalho(models.Model):
    apelido = models.CharField(max_length=500)
    imagem = models.ImageField(upload_to="cabecalho/", null=True, blank=True)
    instituicao = models.CharField(max_length=300)
    data = models.DateField(null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    turma = models.CharField(max_length=150, null=True, blank=True)
    nome_estudante = models.BooleanField()
    nome_docente = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.apelido)

    class Meta:
        db_table = "cabecalho"

class Prova(models.Model):
    nome = models.CharField(max_length=500)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=False)
    observacao = models.TextField(null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="professor")
    cabecalho = models.ForeignKey(Cabecalho, on_delete=models.PROTECT, default="")
    questao = models.ManyToManyField(Questao)
    tipo = models.CharField(max_length=4)
    #questao = models.ForeignKey(Questao, on_delete=models.PROTECT, default="")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "prova"
        verbose_name_plural = "Provas"



class Gabarito(models.Model):
    prova = models.ForeignKey(Prova,on_delete=models.CASCADE, related_name="prova")
    questoes = models.ManyToManyField(Questao)
    alternativa_correta = models.ManyToManyField(Alternativa)

    def __str__(self):
        return str(self.id)



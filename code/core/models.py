from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Area(models.Model):
    area = models.CharField(max_length=400)

    def __str__(self):
        return str(self.area)

    class Meta:
        db_table = "area"

class Disciplina(models.Model):
    disciplina = models.CharField(max_length=250)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.disciplina)

    class Meta:
        db_table = "disciplina"

class Assunto(models.Model):
    assunto = models.CharField(max_length=400)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.assunto)

    class Meta:
        db_table = "assunto"

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
    #senha = models.CharField(max_length=10)
    nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    foto = models.ImageField(upload_to="professor/", null=True, blank=True)
    disciplina = models.ManyToManyField(Disciplina)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = "professor"
        verbose_name_plural = "Professores"


class Questao(models.Model):
    enunciado = models.TextField()
    #enunciado = HTMLField()
    #enunciado = RichTextUploadingField()
    imagem = models.ImageField(upload_to="questao/", null=True, blank=True)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE)
    origem = models.ForeignKey(Origem, on_delete=models.CASCADE, blank=True, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.enunciado)

    class Meta:
        db_table = "questao"
        verbose_name_plural = "Questões"

class Alternativa(models.Model):
    alternativa = models.TextField()
    correta = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to="alternativa/", null=True, blank=True)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')
    letra = models.CharField(max_length=1)

    def __str__(self):
        return str(self.alternativa)

    class Meta:
        db_table = "alternativa"


class Texto(models.Model):
    texto = models.TextField()
    referencia = models.CharField(max_length=800, blank=True, null=True)
    #assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='textos')

    def __str__(self):
        return str(self.texto)

    class Meta:
        db_table = "texto"
        verbose_name_plural = "Textos"


class Configuracoes(models.Model):
    apelido = models.CharField(max_length=500)
    cabecalho = models.TextField()
    imagem_cabecalho = models.ImageField(upload_to="cabecalho/", null=True, blank=True)
    rodape = models.TextField(null=True, blank=True)
    imagem = models.ImageField(upload_to="rodape/", null=True, blank=True)
    tamanho = models.IntegerField()

    def __str__(self):
        return str(self.cabecalho)

    class Meta:
        db_table = "configuracoes"

class Prova(models.Model):
    #instituicao = models.CharField(max_length=300)
    apelido = models.CharField(max_length=500)
    data = models.DateField()
    valor = models.FloatField(null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=False)
    observacao = models.TextField(null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="professor")
    configuracoes = models.ForeignKey(Configuracoes, on_delete=models.PROTECT, default="")
    questao = models.ManyToManyField(Questao)
    #questao = models.ForeignKey(Questao, on_delete=models.PROTECT, default="")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "prova"
        verbose_name_plural = "Provas"


#Inserir descrição para as provas
#Inserir nome para as provas

class Gabarito(models.Model):
    prova = models.ForeignKey(Prova,on_delete=models.CASCADE, related_name="prova")
    questoes = models.ManyToManyField(Questao)
    alternativa_correta = models.ManyToManyField(Alternativa)

    def __str__(self):
        return str(self.id)
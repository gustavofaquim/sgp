from django.db import models
from tinymce.models import HTMLField
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


class Area(models.Model):
    area = models.CharField(max_length=400)

    def __str__(self):
        return str(self.area)

    class Meta:
        db_table = "area"


class Professor(models.Model):
    user = models.ForeignKey(User, related_name='professor', unique=True, on_delete=models.CASCADE)
    cpf = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=350)
    email = models.EmailField()
    #senha = models.CharField(max_length=10)
    nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    foto = models.ImageField(upload_to="ft_prof", null=True, blank=True)
    disciplina = models.ManyToManyField(Disciplina)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = "professor"
        verbose_name_plural = "Professores"




class Questao(models.Model):
    #enunciado = models.TextField()
    #enunciado = HTMLField()
    enunciado  = RichTextUploadingField ()
    imagem = models.ImageField(upload_to="questao", null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, default="")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, default="")
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.enunciado)

    class Meta:
        db_table = "questao"
        verbose_name_plural = "Questões"

class Alternativa(models.Model):
    alternativa = models.TextField()
    correta = models.BooleanField(default="False")
    imagem = models.ImageField(upload_to="alternativa/", null=True, blank=True)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')

    def __str__(self):
        return str(self.alternativa)

    class Meta:
        db_table = "alternativa"


class Configuracoes(models.Model):
    cabecalho = models.TextField()
    rodape = models.TextField()
    TIPO_FONTE = (
        ('AR','Arial'),
        ('TR','Times New Roman'),
        ('HL','Helvetica'),
        ('VD','Verdana'),
        ('CL','Calibri'),
        ('TH','Tahoma')
    )
    tipo_fonte = models.CharField(max_length=2, choices= TIPO_FONTE)
    tamanho = models.IntegerField()

    def __str__(self):
        return str(self.cabecalho)

    class Meta:
        db_table = "configuracoes"

class Prova(models.Model):
    #instituicao = models.CharField(max_length=300)
    data = models.DateField()
    valor = models.FloatField(null=True, blank=True)
    observacao = models.TextField()
    imagem = models.ImageField(upload_to="prova", null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="professor")
    configuracoes = models.ForeignKey(Configuracoes, on_delete=models.PROTECT, default="")
    questao = models.ManyToManyField(Questao)
    #questao = models.ForeignKey(Questao, on_delete=models.PROTECT, default="")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "prova"
        verbose_name_plural = "Avaliações"

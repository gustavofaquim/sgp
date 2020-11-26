from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile


class OrigemForm(forms.ModelForm):
    class Meta:
        model = Origem
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class SubCategoriaForm(forms.ModelForm):
    class Meta:
        model = SubCategoria
        fields = '__all__'


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('cpf','nome','email','nascimento','foto','disciplina')
        foto = forms.ImageField()


class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'
        imagem = forms.ImageField()


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['nome','enunciado','categoria','subcategoria','origem','tag']


class CabecalhoForm(forms.ModelForm):
    class Meta:
        model = Cabecalho
        fields = '__all__'

class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['nome','observacao','disciplina','cabecalho','questao', 'tipo']
        widgets = {
            'questao': forms.CheckboxSelectMultiple(attrs={
            'id': 'questoes',
            'class': 'questoes'})
        }


from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile



class FormTeste(forms.Form):
    nome = forms.CharField(label='nome', max_length=200)
    imagem = forms.ImageField(label='foto')

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
        foto = forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file-input'}))
        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'nascimento': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'disciplina': forms.CheckboxSelectMultiple(attrs={'class': 'select-disciplina'}),
            }

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'
        imagem = forms.ImageField()
        widgets={
            'alternativa': forms.Textarea(attrs={'class':'form-control'}),
            'letra': forms.TextInput(attrs={'class':'form-control'}),
        }


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['nome','enunciado','categoria','subcategoria','origem','tag']
        widgets={
            'enunciado': forms.Textarea(attrs={'class':'form-control'}),
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'origem': forms.SelectMultiple(attrs={'class':'custom-select mr-sm-2'}),
            'categoria': forms.SelectMultiple(attrs={'class': 'custom-select mr-sm-2'}),
            'subcategoria': forms.SelectMultiple(attrs={'class': 'custom-select mr-sm-2'}),
            'tag': forms.SelectMultiple(attrs={'class': 'custom-select mr-sm-2'}),
        }


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
            'id': 'questoes customCheck1',
            'class': 'questoes'}),
            'disciplina': forms.SelectMultiple(attrs={'class':'form-control'}),
            'cabecalho': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class':'form-control'})
        }


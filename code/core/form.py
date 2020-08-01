from django import forms
from django.contrib.auth.models import User

from .models import Professor
from .models import Alternativa
from .models import Questao
from .models import Prova
from .models import Area
from django.core.files.uploadedfile import SimpleUploadedFile

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('cpf','nome','email','nascimento','foto','disciplina')
        foto = forms.FileField(
            label='Selecione sua foto'
        )

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'
        imagem = forms.ImageField()


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        #fields = '__all__'
        fields = ['enunciado','imagem','area','disciplina']



class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        #fields = '__all__'
        fields = ['data','valor','observacao','imagem','configuracoes','questao']


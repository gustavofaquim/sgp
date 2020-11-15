from django import forms
from django.contrib.auth.models import User

from .models import Professor
from .models import Alternativa
from .models import Questao
from .models import Prova
from .models import Area
from .models import Configuracoes
from .models import Assunto
from .models import Texto
from django.core.files.uploadedfile import SimpleUploadedFile

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'

class AssuntoForm(forms.ModelForm):
    class Meta:
        model = Assunto
        fields = '__all__'

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('cpf','nome','email','nascimento','foto','disciplina','foto')
        foto = forms.ImageField()


class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'
        imagem = forms.ImageField()

class TextoForm(forms.ModelForm):
    class Meta:
        model = Texto
        fields = '__all__'


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['enunciado','imagem','assunto']
        imagem = forms.ImageField()



class ConfiguracoesForm(forms.ModelForm):
    class Meta:
        model = Configuracoes
        fields = '__all__'

class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['apelido','data','valor','observacao','disciplina','configuracoes','questao']
        widgets = {
            'questao': forms.CheckboxSelectMultiple(attrs={
            'id': 'questoes',
            'class': 'questoes'})
        }


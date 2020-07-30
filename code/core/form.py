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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'
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
        fields = '__all__'



class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['professor', 'observacao', 'questao', 'configuracoes']


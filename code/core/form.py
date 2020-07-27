from django import forms
from .models import Professor
from .models import Alternativa
from .models import Questao
from .models import Prova

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['cpf', 'nome','email', 'senha', 'nascimento', 'disciplina','foto']
        foto = forms.FileField(
            label='Selecione sua foto'
        )

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = '__all__'


class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['professor', 'observacao', 'questao', 'configuracoes']

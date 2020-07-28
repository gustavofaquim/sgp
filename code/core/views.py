from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import FileResponse
import io
from weasyprint import HTML
from django.http import HttpResponse
import json

from .models import *
from .form import *


def index(request):
    return render(request, 'index.html')

#Curd professor
def cadastro_professor(request):
    form = ProfessorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/lista_professores/')

    return render(request, 'form-professor.html', {'form': form})


def lista_professor(request):
    professores = Professor.objects.all()
    return render(request, 'professor.html', {'professores': professores})

def atualizar_prof(request,cpf):
    professor = Professor.objects.get(cpf=cpf)
    form = ProfessorForm(request.POST or None, instance=professor)

    if form.is_valid():
        form.save()
        return redirect('/lista_professores/')

    return render(request, 'form-professor.html', {'form': form, 'professor': professor})

def deletar_prof(request,cpf):
    professor = Professor.objects.get(cpf=cpf)
    professor.delete()
    return redirect('/lista_professores/')


#Crud alternativa
def cadastro_alternativa(request):

    form_alternativa = AlternativaForm(request.POST or None)
    form_questao = QuestaoForm(request.POST or None)

    if form_alternativa.is_valid():
        if form_questao.is_valid():
            questao = form_questao.save()
            #print(questao.id)   #Pega o ID da última questão salva no BD.
            nova_questao = Questao.objects.get(id=questao.id)
            alternativa = form_alternativa.cleaned_data['alternativa'] #Pegar campo alternativa do form
            correta = form_alternativa.cleaned_data['correta']
            nova_alternativa = Alternativa(alternativa = alternativa,  correta = correta, questao = nova_questao)

            #print ("Questão: ", nova_questao.enunciado , " Area: ", nova_questao.area, " ID: ", nova_questao.id, "\n")
            #print("Alternativa: " , nova_alternativa.alternativa , " Correta: " , nova_alternativa.correta, "Questao: ", nova_alternativa.questao.id)
            nova_alternativa.save()
            #form_alternativa.save()

        return redirect('/lista_questao/')


    return render(request, 'form-questao.html', {'form_alternativa': form_alternativa, 'form_questao': form_questao})


def lista_alternativa(request):
    alternativas = Alternativa.objects.all()
    return render(request, 'alternativa.html', {'alternativas': alternativas})


def atualizar_alter(request,id):
    alternativa = Alternativa.objects.get(id=id)
    form = AlternativaForm(request.POST or None, instance=alternativa)

    if form.is_valid():
        form.save()
        return redirect('/lista_alternativas/')

    return render(request, 'form-alternativa.html', {'form': form, 'alternativa': alternativa})

def deletar_alter(request,id):
    alternativa = Alternativa.objects.get(id=id)
    alternativa.delete()
    return redirect('/lista_alternativas/')


#Crud questao

def cadastro_questao(request):
    if request.method == "GET":
        form = QuestaoForm()
        form_alternativa_factory = inlineformset_factory(Questao,Alternativa,form=AlternativaForm, extra=5)
        form_alternativa = form_alternativa_factory()

        context = {
           'form': form,
           'form_alternativa': form_alternativa,
        }
        return render(request, "form-questao.html", context)

    elif request.method == "POST":
        form = QuestaoForm(request.POST,request.FILES)
        form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm)
        form_alternativa = form_alternativa_factory(request.POST,request.FILES)

        if form.is_valid() and form_alternativa.is_valid():
            questao = form.save()
            form_alternativa.instance = questao
            form_alternativa.save()
            return redirect(reverse('questao.html'))
        else:
            context = {
                'form': form,
                'form_telefone': form_alternativa,
            }
            return render(request,'form-questao.html', context)


def atualizar_quest(request,questao_id):
    if request.method == "GET":
        objeto = Questao.objects.filter(id=questao_id).first()

        if objeto is None:
            return redirect(reverse('questao.html'))

        form = QuestaoForm(instance=objeto)
        form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm, extra=0)
        form_alternativa = form_alternativa_factory(instance=objeto)

        context = {
            'form': form,
            'form_alternativa': form_alternativa,
        }
        return render(request, "form-questao.html", context)

    elif request.method == "POST":
        objeto = Questao.objects.filter(id=questao_id).first()
        if objeto is None:
            return redirect(reverse('lista_questao'))

        form = QuestaoForm(request.POST, instance=objeto)
        form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm)
        form_alternativa = form_alternativa_factory(request.POST, instance=objeto)

        if form.is_valid() and form_alternativa.is_valid():
            questao = form.save()
            form_alternativa.instance = questao
            form_alternativa.save()
            return redirect(reverse('lista_questao'))

        else:
            context = {
                'form': form,
                'form_alternativa': form_alternativa,
            }
            return render(request, "form-questao.html", context)


def lista_questao(request):
    questoes = Questao.objects.all()
    return render(request, 'questao.html', {'questoes': questoes})

def deletar_quest(request,id):
    questao = Questao.objects.get(id=id)
    questao.delete()
    return redirect('/lista_questao/')


#Crud prova
def cadastro_prova(request):
    form = ProvaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/lista_prova/')

    return render(request, 'form-prova.html', {'form': form})

def lista_prova(request):
    provas = Prova.objects.all()
    return render(request, 'prova.html', {'provas': provas})

def atualizar_prov(request,id):
    prova = Prova.objects.get(id=id)
    form = ProvaForm(request.POST or None, instance=prova)

    if form.is_valid():
        form.save()
        return redirect ('/lista_prova/')

    return render(request, 'form-prova.html', {'form': form, 'prova': prova})

def gerar_prova(request, id):
    prova = Prova.objects.get(id=id)
    tamanho = prova.configuracoes.tamanho
    fonte = prova.configuracoes.tipo_fonte

    html_string = render_to_string('prova/modelo1.html', {'prova': prova,'tamanho':json.dumps(tamanho), 'fonte':json.dumps(fonte)})
    print(prova.professor.nome)
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    html.write_pdf(target='/tmp/{}.pdf'.format(prova));

    fs = FileSystemStorage('/tmp')
    with fs.open('{}.pdf'.format(prova)) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(prova)
        return response

    return response


def vizualiar_prova(request, id):
    print("Ola mundo")
    prova = Prova.objects.get(id=id)
    tamanho = prova.configuracoes.tamanho
    fonte = prova.configuracoes.tipo_fonte
    return render(request,'prova/modelo1.html', {'prova': prova, 'tamanho':json.dumps(tamanho), 'fonte':json.dumps(fonte)})


def deletar_prov(request,id):
    prova = Prova.objects.get(id=id)
    prova.delete()
    return redirect('/lista_prova/')


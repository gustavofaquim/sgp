from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
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
from django.http import JsonResponse

def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})

@login_required(login_url='/login')
def deslogar_usuario(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login')
def filtro_categoria(request):
    professor = Professor.objects.get(user_id=request.user)
    ids = []
    aux = Categoria.objects.filter(disciplina=0)

    for disciplinas in professor.disciplina.all():
        ids.append(disciplinas.id)
        categorias = aux | Categoria.objects.filter(disciplina=disciplinas.id)

    form = ProvaForm()

    form.fields["categoria"].queryset = categorias
    form.fields["disciplina"].queryset = professor.disciplina


@login_required(login_url='/login')
def busca_questao(request):

    if request.method == "GET":
        query_original = request.GET.get('term')
        questoes = Questao.objects.filter(nome__icontains=query_original)
        mylist = []
        mylist += [x.nome for x in questoes]

        return JsonResponse(mylist, safe=False)

    if request.method=="POST":

        search_str=json.loads(request.body).get('busca')

        questoes = Questao.objects.filter(
            nome__icontains=search_str, professor=request.user) | Questao.objects.filter(
            enunciado__icontains=search_str, professor=request.user) | Questao.objects.filter(
            categoria__icontains=search_str, professor=request.user) | Questao.objects.filter(
            subcategoria__icontains=search_str, professor=request.user) | Questao.objects.filter(
            origem__icontains=search_str, professor=request.user) | Questao.objects.filter(
            tag__icontains=search_str, professor=request.user)

        data = questoes.values()
        return JsonResponse(list(data), safe=False)



@login_required(login_url='/login')
def cadastrar_origem(request):
    form = OrigemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/cadastro-questao/')
    return render(request, 'forms.html', {'form':form})




@login_required(login_url='/login')
def cadastrar_categoria(request):

    form = CategoriaForm(request.POST or None)
    professor = Professor.objects.get(user_id=request.user)
    ids = []
    aux = Disciplina.objects.filter(id=0)

    for disciplinas in professor.disciplina.all():
        ids.append(disciplinas.id)
        disciplinas = aux | Disciplina.objects.filter(id=disciplinas.id)

    form.fields["disciplina"].queryset = disciplinas

    if form.is_valid():
        form.save()
        return redirect('/cadastro-questao/')
    return render(request, 'forms.html',{'form': form})


#CRUD DISCIPLINAS
@login_required(login_url='/login')
def lista_disciplina(request):
    disciplina = Disciplina.objects.all()
    area = Area.objects.all()
    return (request, 'lista.html', {'disciplina': disciplina, 'area': area})

#Crud professor


def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        form_professor = ProfessorForm(request.POST,request.FILES)

        if form_usuario.is_valid() and form_professor.is_valid():

            professor = form_professor.save(commit=False)
            usuario = form_usuario.save(commit=False)
            usuario.username = professor.email

            usuario.save()

            usuario_id = User.objects.get(id=usuario.id)
            professor.user = usuario_id

            professor.save()

            if hasattr(form_professor, 'save_m2m'):
                form_professor.save_m2m()

            return redirect('index')
    else:
        form_usuario = UserCreationForm()
        form_professor = ProfessorForm()
    return render(request, 'cadastro.html', {'form_usuario': form_usuario, 'form_professor': form_professor})

@login_required(login_url='/login')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})


@login_required(login_url='/login')
def atualizar_prof(request,id):
    professor = Professor.objects.get(user_id=id)
    print(request.method)

    form = ProfessorForm(request.POST or None, request.FILES or None, instance=professor)
    print(request.FILES)
    print(form.is_valid())
    if form.is_valid():
        forms = form.save(commit=False)
        forms.save()
        return redirect('index')

    return render(request, 'form-professor.html', {'form': form, 'professor': professor})


@login_required(login_url='/login')
def deletar_prof(request,cpf):
    professor = Professor.objects.get(cpf=cpf)
    user = User.objects.get(id=professor.user.id)
    professor.delete()
    user.delete()

    return redirect('index')



#Crud alternativa
@login_required(login_url='/login')
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

@login_required(login_url='/login')
def lista_alternativa(request):
    alternativas = Alternativa.objects.all()
    return render(request, 'alternativa.html', {'alternativas': alternativas})

@login_required(login_url='/login')
def atualizar_alter(request,id):
    alternativa = Alternativa.objects.get(id=id)
    form = AlternativaForm(request.POST or None, request.FILES or None, instance=alternativa)

    if form.is_valid():
        form.save()
        return redirect('/lista_alternativas/')

    return render(request, 'form-alternativa.html', {'form': form, 'alternativa': alternativa})

@login_required(login_url='/login')
def deletar_alter(request,id):
    alternativa = Alternativa.objects.get(id=id)
    alternativa.delete()
    return redirect('/lista_alternativas/')


#Crud questao
@login_required(login_url='/login')
def cadastro_questao(request):
    if request.method == "GET":
        professor = Professor.objects.get(user_id=request.user)
        ids = []
        aux = Categoria.objects.filter(disciplina=0)
        categorias = aux #apagar essa linha se bugar

        for disciplinas in professor.disciplina.all():
            ids.append(disciplinas.id)
            categorias = aux | Categoria.objects.filter(disciplina=disciplinas.id)

        form = QuestaoForm()

        form.fields["categoria"].queryset = categorias
        form_alternativa_factory = inlineformset_factory(Questao,Alternativa,form=AlternativaForm, extra=1)
        form_alternativa = form_alternativa_factory()
        #form_texto_factory = inlineformset_factory(Questao, Texto, form=TextoForm, extra=1)
        #form_texto = form_texto_factory()


        context = {
           'form': form,
           'form_alternativa': form_alternativa,
           #'form_texto': form_texto,
        }


        return render(request, "form-questao.html", context)

    elif request.method == "POST":
        form = QuestaoForm(request.POST,request.FILES)
        form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm)
        form_alternativa = form_alternativa_factory(request.POST,request.FILES)

        if form.is_valid() and form_alternativa.is_valid():
            questao = form.save(commit=False)
            professor = Professor.objects.get(user_id=request.user)
            questao.professor = professor

            questao.save()

            form_alternativa.instance = questao
            form_alternativa.save()

            return redirect(reverse('lista_questao'))
        else:
            context = {
                'form': form,
                'form_alternativa': form_alternativa, #mudar primeiro para form_telefone se der algum erro
            }
            return render(request,'form-questao.html', context)



@login_required(login_url='/login')
def atualizar_quest(request,questao_id):
    if request.method == "GET":
        objeto = Questao.objects.filter(id=questao_id).first()

        if objeto is None:
            return redirect(reverse('questao.html'))

        form = QuestaoForm(request.FILES or None,instance=objeto)
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

        form = QuestaoForm(request.POST,request.FILES, instance=objeto)
        form_alternativa_factory = inlineformset_factory(Questao, Alternativa, form=AlternativaForm)
        form_alternativa = form_alternativa_factory(request.POST,request.FILES, instance=objeto)

        print("\n\n\n",form_alternativa.errors,"\n\n\n")
        
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

@login_required(login_url='/login')
def lista_questao(request):

    professor = Professor.objects.get(user_id=request.user)
    questoes = Questao.objects.filter(professor=professor)

    busca = request.GET.get("busca")
    if busca:
        questoes = Questao.objects.filter(nome__icontains=busca)

    return render(request, 'questao.html', {'questoes': questoes})

@login_required(login_url='/login')
def deletar_quest(request,id):
    questao = Questao.objects.get(id=id)
    questao.delete()
    return redirect('/lista_questao/')

@login_required(login_url='/login')
def cadastro_cabecalho(request):
    if request.method == "GET":
        form = CabecalhoForm()

        context = {
            'form': form,
        }

        return render(request, "form.html", context)

    elif request.method == "POST":
        form = CabecalhoForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/index/')

        return render(request, 'form.html', {'form': form})

#Crud prova
@login_required(login_url='/login')
def cadastro_prova(request):

    if request.method == "GET":
        professor = Professor.objects.get(user_id=request.user)
        ids = []
        aux = Categoria.objects.filter(disciplina=0)
        aux2 = Questao.objects.filter(categoria=0)
        questoes = Questao.objects.filter(categoria=0)


        for disciplinas in professor.disciplina.all():
            ids.append(disciplinas.id)
            categorias = aux | Assunto.objects.filter(disciplina=disciplinas.id)
            for categoria_quest in categorias:
                #print(assunt_quest)
                questoes = questoes| aux2 | Questao.objects.filter(categoria=categoria_quest.id)


        form = ProvaForm()


        form.fields["disciplina"].queryset = professor.disciplina
        form.fields["questao"].queryset = questoes


        context = {
            'form': form,
        }
        return render(request, "form-prova.html", context)

    elif request.method == "POST":
        form = ProvaForm(request.POST, request.FILES)

        if form.is_valid():
            prova = form.save(commit=False)
            professor = Professor.objects.get(user_id=request.user)
            prova.professor = professor
            prova.save()

            if hasattr(form, 'save_m2m'):
                form.save_m2m()

            return redirect('/lista_prova/')

        return render(request, 'form-prova.html', {'form': form})


@login_required(login_url='/login')
def atualizar_prov(request,id):

    professor = Professor.objects.get(user_id=request.user)
    ids = []
    aux = Categoria.objects.filter(disciplina=0)
    aux2 = Questao.objects.filter(categoria=0)

    for disciplinas in professor.disciplina.all():
        ids.append(disciplinas.id)
        categorias = aux | Categoria.objects.filter(disciplina=disciplinas.id)
        for categoria_quest in categorias:
            questoes = aux2 | Questao.objects.filter(categoria=categoria_quest.id)


    prova = Prova.objects.get(id=id)
    form = ProvaForm(request.POST or None, request.FILES or None, instance=prova)

    form.fields["disciplina"].queryset = professor.disciplina
    form.fields["questao"].queryset = questoes

    if form.is_valid():
        form.save()
        return redirect ('/lista_prova/')

    return render(request, 'form-prova.html', {'form': form, 'prova': prova})


@login_required(login_url='/login')
def lista_prova(request):
    professor = Professor.objects.get(user=request.user)
    provas = Prova.objects.filter(professor=professor)
    return render(request, 'prova.html', {'provas': provas})


@login_required(login_url='/login')
def gerar_prova(request, id):
    prova = Prova.objects.get(id=id)
    #tamanho = prova.configuracoes.tamanho
    #fonte = prova.configuracoes.tipo_fonte

    #html_string = render_to_string('prova/modelo1.html', {'prova': prova,'tamanho':json.dumps(tamanho), 'fonte':json.dumps(fonte)})
    html_string = render_to_string('prova/modelo1.html', {'prova': prova})
    print(prova.professor.nome)
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    html.write_pdf(target='/tmp/{}.pdf'.format(prova))

    fs = FileSystemStorage('/tmp')
    with fs.open('{}.pdf'.format(prova)) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(prova)
        return response

@login_required(login_url='/login')
def gerar_gabarito(request,id):

    prova = Prova.objects.get(id=id)
    #print(prova.questao.all())

    lista_questoes = []
    alternativa_correta = []


    for questoes in prova.questao.all():

        print(questoes.enunciado)
        print(questoes.alternativas.all().filter(correta=True))
        #lista_questoes.append(Questao.objects.get(id=questoes.id))
        #alternativa_correta.append(questoes.alternativas.filter(correta = True))
        #Gabarito.alternativa_correta.set(alternativa_correta)

    #gabarito = Gabarito(prova=prova, questoes = lista_questoes, alternativa_correta = alternativa_correta)

    #questao = Questao.objects.get(id=prova.questao.id)


    #print(questao.alternativas.all())

    #gabarito = Gabarito.objects.create(prova=prova,questao=questao)
    #gabarito = Gabarito(prova=prova,questao=questao,alternativa=alternativa)

    #print("\n\n", gabarito.prova.questao.enunciado,"\n\n\n")

    #html_string = render_to_string('prova/gabarito.html', {'gabarito': gabarito})

    return redirect('/index')



@login_required(login_url='/login')
def vizualiar_prova(request, id):
    print("Ola mundo")
    prova = Prova.objects.get(id=id)
    tamanho = prova.configuracoes.tamanho
    fonte = prova.configuracoes.tipo_fonte
    return render(request,'prova/modelo1.html', {'prova': prova, 'tamanho':json.dumps(tamanho), 'fonte':json.dumps(fonte)})

@login_required(login_url='/login')
def deletar_prov(request,id):
    prova = Prova.objects.get(id=id)
    prova.delete()
    return redirect('/lista_prova/')


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core import views
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.logar_usuario, name='login'),
    path('logout',views.deslogar_usuario, name='logout'),
    #CRUD AREA
    path('cadastro_area/', views.cadastro_area),
    path('cadastrar-categoria/', views.cadastrar_categoria, name='cadastrar-categoria'),
    path('cadastrar-origem/', views.cadastrar_origem, name='cadastrar-origem'),
    path('cadastrar-texto/', views.cadastrar_texto, name='cadastrar-texto'),
    path('lista_disciplina/', views.lista_disciplina, name='lista_disciplina'),
    #Crud professor
    path('cadastrar_usuario/', views.cadastrar_usuario, name="cadastrar_usuario"),
    path('alterar_senha', views.alterar_senha, name='alterar_senha'),
    path('atualizar_professor/<int:id>/', views.atualizar_prof, name='atualizar_professor'),
    path('deletar_professor/<int:cpf>', views.deletar_prof, name='deletar_professor'),
    path('cadastro-questao/', views.cadastro_questao, name='cadastro-questao'),
    #path('cadastro_assunto/', views.cadastro_questao, name='cadastro-assunto'),
    path('lista_questao/', views.lista_questao, name='lista_questao'),
    path('atualizar_questao/<int:questao_id>', views.atualizar_quest, name='atualizar_questao'),
    path('deletar_questao/<int:id>', views.deletar_quest, name='deletar_questao'),
    #Crud prova
    path('cadastro_cabecalho/', views.cadastro_cabecalho, name='cadastro_cabecalho'),
    path('cadastro-prova/', views.cadastro_prova),
    path('lista_prova/', views.lista_prova, name='lista_prova'),
    path('atualizar_prova/<int:id>', views.atualizar_prov, name='atualizar_prova'),
    path('deletar_prova/<int:id>', views.deletar_prov, name='deletar_prova'),
    path('gerar_prova/<int:id>', views.gerar_prova, name="gerar_prova"),
    path('gerar_gabarito/<int:id>', views.gerar_gabarito, name="gerar_gabarito"),
    path('vizualiar_prova/<int:id>', views.vizualiar_prova, name="vizualiar_prova"),
    ####
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #path(r'^tinymce/', include('tinymce.urls')),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
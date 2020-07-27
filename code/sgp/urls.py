
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', views.user_login),
    #path('login/submit', views.submit_login),
    #path('logout/', views.user_logout),
    #Crud professor
    path('cadastro-professor/', views.cadastro_professor),
    path('lista_professores/', views.lista_professor),
    path('atualizar_professor/<int:cpf>/', views.atualizar_prof, name='atualizar_professor'),
    path('deletar_professor/<int:cpf>', views.deletar_prof, name='deletar_professor'),
    #Crud alternativa
    path('cadastro-alternativa/', views.cadastro_alternativa),
    path('lista_alternativas/', views.lista_alternativa),
    path('atualizar_alternativa/<int:id>/', views.atualizar_alter, name='atualizar_alternativa'),
    path('deletar_alternativa/<int:id>/', views.deletar_alter, name='deletar_alternativa'),
    #Crud questao
    path('cadastro-questao/', views.cadastro_questao),
    path('lista_questao/', views.lista_questao, name='lista_questao'),
    path('atualizar_questao/<int:questao_id>', views.atualizar_quest, name='atualizar_questao'),
    path('deletar_questao/<int:id>', views.deletar_quest, name='deletar_questao'),
    #Crud prova
    path('cadastro-prova/', views.cadastro_prova),
    path('lista_prova/', views.lista_prova),
    path('atualizar_prova/<int:id>', views.atualizar_prov, name='atualizar_prova'),
    path('deletar_questao/<int:id>', views.deletar_prov, name='deletar_prova'),
    path('questao_alterntiva/<int:questao_id>', views.questao_alterntiva),
    path('questao_alterntivas/', views.questao_alterntivas),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #path(r'^tinymce/', include('tinymce.urls')),
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

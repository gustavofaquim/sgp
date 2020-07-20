from itertools import count

from django.contrib import admin
from .models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django_object_actions import DjangoObjectActions

#tabularinline ou stackedinline

class AlternativaAdmin(admin.StackedInline):
    model = Alternativa
    list_filter = ['correta', 'questao']
    max_num = 4
    extra = 6

class QuestaoAdmin(admin.ModelAdmin):
    inlines = [AlternativaAdmin]
    fields = ['enunciado','imagem','professor',('area','disciplina')]
    list_display = ('enunciado','disciplina')
    search_fields = ['enunciado']
    #save_on_top = True


class ProvaAdmin(DjangoObjectActions,admin.ModelAdmin):
    filter_horizontal = ("questao",)


    def generate_pdf(self, request, prova):


        print(prova.questao.get(id=2).imagem)

        html_string = render_to_string('prova/modelo1.html', {'prova': prova})
        html = HTML(string=html_string,base_url=request.build_absolute_uri('/'))
        html.write_pdf(target='/tmp/{}.pdf'.format(prova));
        
        fs = FileSystemStorage('/tmp')
        with fs.open('{}.pdf'.format(prova)) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(prova)
            return response

        return response

    generate_pdf.label = 'Gerar PDF'
    generate_pdf.short_description = 'Clique para gerar o PDF da prova'

    change_actions = ('generate_pdf',)




admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Alternativa)
admin.site.register(Disciplina)
admin.site.register(Professor)
admin.site.register(Prova, ProvaAdmin)
'''
AQUI TAVA TUDO BEM

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['id', 'disciplina']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'professor', 'email']

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_dsplay = ['enunciado','imagem','area','disciplina']

@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    list_display = ['alternativa', 'correta', 'imagem', 'questao']

@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ['configuracoes', 'observacao', 'questao'] '''
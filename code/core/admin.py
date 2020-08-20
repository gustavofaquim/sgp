import json
from django.core import serializers
from itertools import count
from django.shortcuts import render
from io import BytesIO
from django.contrib import admin
from weasyprint.pdf import pdf_format, PDFFile

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
    max_num = 5
    extra = 8

class QuestaoAdmin(admin.ModelAdmin):
    inlines = [AlternativaAdmin]
    fields = ['enunciado','imagem','professor','assunto']
    list_display = ['enunciado']
    search_fields = ['enunciado']
    #save_on_top = True


class ProvaAdmin(DjangoObjectActions,admin.ModelAdmin):
    filter_horizontal = ("questao",)


    def generate_pdf(self, request, prova):


        #print(prova.questao.get(id=2).imagem)

        html_string = render_to_string('prova/modelo1.html', {'prova': prova})
        html = HTML(string=html_string,base_url=request.build_absolute_uri('/'))
        html.write_pdf(target='/tmp/{}.pdf'.format(prova));
        
        fs = FileSystemStorage('/tmp')
        with fs.open('{}.pdf'.format(prova)) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(prova)
            return response

        return response


    def vizualiar_prova(self, request, prova):
       print("Ola mundo")
       tamanho = prova.configuracoes.tamanho
       fonte = prova.configuracoes.tipo_fonte
       return render(request,'prova/modelo1.html', {'prova': prova, 'tamanho':json.dumps(tamanho), 'fonte':json.dumps(fonte)})



    vizualiar_prova.label = 'Ver Prova'

    generate_pdf.label = 'Gerar PDF'

    generate_pdf.short_description = 'Clique para gerar o PDF da prova'

    change_actions = ('generate_pdf','vizualiar_prova')




admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Alternativa)
admin.site.register(Disciplina)
admin.site.register(Professor)
admin.site.register(Area)
admin.site.register(Configuracoes)
admin.site.register(Prova, ProvaAdmin)
admin.site.register(Assunto)

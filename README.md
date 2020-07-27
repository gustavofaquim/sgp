# Sistema Gerador de Provas

### Configurações do banco de dados
Ver em **sgp/settings.py**.


### Instalação dos pacotes (dependências)

```
pip install -r requirements.txt
```


### Atualizar lista de pacotes (dependências)
```
pip freeze > requirements.txt
```


### Para iniciar o servidor
```
python manage.py runserver
```


### Para criar um superusuário
```
python manage.py createsuperuser
```


### Para criar uma nova aplicação
```
python manage.py startapp blog
```


### Preparar arquivo de migração (após alterar um modelo)
```
python manage.py makemigrations nomeApp
```


### Aplicar arquivo de migração
```
python manage.py migrate nomeApp
```
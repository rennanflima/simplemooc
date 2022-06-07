# Simple Mooc

Projeto desenvolvido no Curso Python 3 na Web com Django (Básico e Intermediário)

### Clonar

Clone este repositório para a sua máquina local

```sh
$ git clone git@github.com:rennanflima/simplemooc.git
```

### Devolpment Setup

Crie o ambiente virtual e instale as dependências:

```sh
$ cd simplemooc
$ make install_deps
```

Configure a instância com o `.env`, fazendo uma copia do arquivo:

```sh
$ cp contrib/env-sample .env
```

> Em caso de dúvidas acesse a página do pacote Python [python-decouple](https://pypi.org/project/python-decouple/)

Gere uma nova SECRET_KEY com o comando abaixo, e copie o seu valor:

```sh
$ python manage.py generate_secret_key
```

Edite o arquivo `.env` e adicine `SECRET_KEY=` com o valor da chave gerada pelo comando anterior e adicione a linha `DEBUG=True`, se for no ambiente de desenvolvimento

```sh
$ vim .env
```

Rodar os testes:

```sh
$ make test
```

Criar banco de dados (Tenha certeza que esteja no mesmo diretório que manage.py)

```
$ python manage.py migrate
```

Criar superusuário

```
$ python manage.py createsuperuser
```

Execute o servidor localmente:

```
$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
October 28, 2021 - 17:00:48
Django version 3.2.8, using settings 'simplemooc.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Configuração

Item | Versão 
---------|-----------
Python | 3.10
Django | 3.2 (LTS)
Pip | última versão

# Simple Mooc

Projeto desenvolvido no Curso Python 3 na Web com Django (Básico e Intermediário)

O *Simple Massive Open Online Course* (Simple Mooc) é uma plataforma simples para o ensino a distância, focada em cursos abertos e massivos.

#### Funcionalidades

- Sistema de aulas: Criação, edição e remoção de aulas e módulos associadas a um curso. Os materiais de aula poderão ser vídeo-aulas (youtube, vimeo e etc) ou materiais para dowload (códigos, PDF's, slides...). ;
- Fórum de dúvidas: fórum geral e aberto, com tópicos separados por categoria. Para responder a um tópico o usuário precisa estar logado;
- Sistema de avisos: mural de avisos, onde esses avisos serão enviados para os alunos por e-mail e uma página onde os alunos paderão comentar;
- Sistema de contas (usuários): os usuário poderão realizar o autocadastro e logar no sitema. Após o login, os usuários poderão alterar o seu perfil.

## Devolpment Setup

Para executar localmente siga os passos abaixo:

1. Clone este repositório para a sua máquina local

```sh
$ git clone git@github.com:rennanflima/simplemooc.git
```


2. Crie o ambiente virtual e instale as dependências:

```sh
$ cd simplemooc
$ make install_deps
```

3. Configure a instância com o `.env`, fazendo uma copia do arquivo:

```sh
$ cp contrib/env-sample .env
```

> Em caso de dúvidas acesse a página do pacote Python [python-decouple](https://pypi.org/project/python-decouple/)

4. Gere uma nova SECRET_KEY com o comando abaixo, e copie o seu valor:

```sh
$ python manage.py generate_secret_key
```

5. Edite o arquivo `.env` e adicine `SECRET_KEY=` com o valor da chave gerada pelo comando anterior e adicione a linha `DEBUG=True`, se for no ambiente de desenvolvimento

```sh
$ vim .env
```

6. Criar banco de dados (Tenha certeza que esteja no mesmo diretório que manage.py)

```
$ python manage.py migrate
```

7. Criar superusuário

```
$ python manage.py createsuperuser
```

8. Execute o servidor localmente:

```
$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
October 28, 2021 - 17:00:48
Django version 3.2.8, using settings 'simplemooc.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Testes

Para rodar os testes unitários e de integração execute o comando abaixo:
 
```sh
$ make test
```

## Configuração

Item | Versão 
---------|-----------
Python | 3.10
Django | 3.2 (LTS)
Pip | última versão

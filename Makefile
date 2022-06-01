ARG := $(word 2, $(MAKECMDGOALS) )
PROJECT_NAME=simplemooc
VENV_NAME = .venv
BIN=$(VENV_NAME)/bin
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
INSTALL_STAMP := $(VENV_NAME)/.install.stamp

.DEFAULT_GOAL := help

## @ instalação
.PHONY: venv update_pip install
venv: ## Cria o Vitual Environment se não estiver sido criado
	@python -m venv $(VENV_NAME)

update_pip: venv ## Atualiza o pip, setuptools e wheel
	@$(PIP) install -U pip setuptools wheel

install_deps: update_pip requirements.txt requirements-dev.txt ## Configura e instala as dependecias de desenvolvimento do projeto
	@$(PIP) install --no-cache-dir -U -r requirements-dev.txt
	@touch $(INSTALL_STAMP)


## @ limpeza
.PHONY: clean clean_dumpdata clean_migrations
clean: ## Limpa caches dos arquivos python
	@find . -name '.coverage' -delete
	@find . -name "*.pyc" -exec rm -rf {} \;
	find . -name '*.pyo' -delete
	@find . -name "__pycache__" -delete
	@find . -name ".ipynb_checkpoints" -type d | xargs rm -rf

clean_dumpdata: ## Limpa dumps do banco
	@find ./db_backup -name "*.json" -exec rm -rf {} \;

clean_migrations: ## Limpa as migrações
	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find . -path "*/migrations/*.pyc"  -delete

## @testes
.PHONY: test coverage functional_tests sec
test: $(INSTALL_STAMP) ## Roda testes
	@$(BIN)/python manage.py test $(ARG)

coverage: $(INSTALL_STAMP) ## Roda cobertura de testes
	@$(BIN)/coverage run manage.py test
	@$(BIN)/coverage report
	@$(BIN)/coverage html
	@$(BIN)/coverage xml

functional_tests:$(INSTALL_STAMP) ## Roda testes funcionais com behave
	@$(PYTHON) manage.py behave

sec: $(INSTALL_STAMP) ## Verifica se tem alguma vulnerabilidade nas bibliotecas que foram instaladas
	@$(BIN)/safety check --ignore=41002 --full-report


## @ análise estática
.PHONY: lint_isort pycodestyle
lint_isort: $(INSTALL_STAMP)
	@$(BIN)/isort --diff -c ${PROJECT_NAME}

pycodestyle: $(INSTALL_STAMP)
	@$(BIN)/pycodestyle ${PROJECT_NAME}

lint: lint_isort pycodestyle ## Executa a análise estática isort, pycodestyle
	
	
## @ formatação
.PHONY: isort pyupgrade format
isort: $(INSTALL_STAMP)
	@$(BIN)/isort .
pyupgrade: $(INSTALL_STAMP)
	@$(BIN)/pyupgrade --py37-plus ${PROJECT_NAME}/*.py
format: isort pyupgrade ## Roda a formatação dos arquivos python usando isort e pyupgrade
	

.PHONY: help
help: update_pip
	@if ! $(PIP) list| grep rich; \
	then $(PIP) install rich; \
	fi;
	@$(PYTHON) help.py
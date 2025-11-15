Sistema de Cadastro Escolar em Python

Este projeto é um sistema de gerenciamento escolar desenvolvido em Python, utilizando persistência de dados em SQLite e interface totalmente baseada em linha de comando (CLI). O sistema permite administrar alunos, disciplinas e notas, incluindo operações completas de cadastro, listagem, edição, exclusão e exportação para CSV.

1. Visão Geral

O objetivo do sistema é oferecer um ambiente simples, modular e funcional para controle de informações escolares. Todas as funcionalidades foram desenvolvidas seguindo os requisitos da especificação do trabalho, incluindo:

Persistência de dados

CRUD completo (Create, Read, Update, Delete)

Cadastro e consulta de notas

Exportação de dados em formato CSV

Estrutura modular por arquivos

2. Arquitetura do Projeto

O projeto é dividido em módulos independentes, cada um responsável por uma área específica do sistema:

/projeto
│
├── funcoes.py
├── main.py
│
├── cadastrar_alunos.py
├── cadastrar_disciplinas.py
├── cadastrar_notas.py
├── consultar_notas.py
│
├── banco_de_dados/
│     └── banco_escolar.db
│
└── exportacoes/
      ├── alunos.csv
      ├── disciplinas.csv
      └── notas.csv

3. Descrição dos Módulos
3.1. funcoes.py

Arquivo central do sistema. Responsável por:

Conexão com o banco SQLite

Criação automática das tabelas

Execução simplificada de consultas SQL

Validação de matrícula (12 dígitos)

Listagem de alunos e disciplinas

Exportação genérica de dados para CSV

Limpeza da tela

Todas as operações de banco de dados realizadas nos módulos utilizam as funções aqui definidas.

3.2. cadastrar_alunos.py

Módulo responsável pelo gerenciamento de alunos.

Funcionalidades:

Cadastrar aluno

Listar alunos

Editar aluno (utilizando somente a matrícula)

Excluir aluno

Exportar dados em alunos.csv

A matrícula é tratada como identificador principal, garantindo padronização e facilidade na localização dos registros.

3.3. cadastrar_disciplinas.py

Gerencia as disciplinas cadastradas no sistema.

Funcionalidades:

Cadastrar disciplina

Listar disciplinas

Editar disciplina (via ID)

Excluir disciplina

Exportar para disciplinas.csv

Cada disciplina possui nome, turno, sala e professor.

3.4. cadastrar_notas.py

Controla o registro e gerenciamento das notas dos alunos.

Funcionalidades:

Cadastrar nota

Listar notas

Editar nota

Excluir nota

Exportar para notas.csv

As notas relacionam alunos e disciplinas por meio de JOINs SQL.

3.5. consultar_notas.py

Módulo dedicado para consultas avançadas de notas.

Consultas disponíveis:

Por matrícula

Por nome do aluno

Por disciplina

Exibição geral de todas as notas registradas

3.6. main.py

Arquivo que integra e organiza todos os módulos. Apresenta o menu principal:

Menu Aluno

Menu Disciplinas

Menu Notas

Consulta de Notas

Sair

Cada opção redireciona para o menu correspondente, permitindo navegação simples e clara.

4. Banco de Dados

O sistema utiliza um banco SQLite armazenado em:

banco_de_dados/banco_escolar.db


As tabelas criadas são:

alunos

disciplinas

notas

As tabelas são criadas automaticamente na primeira execução do script, caso ainda não existam.

5. Exportação de Arquivos

Todos os cadastros podem ser exportados para CSV através das funções de exportação presentes nos menus. Os arquivos são gerados na pasta:

exportacoes/


Formato dos arquivos exportados:

alunos.csv

disciplinas.csv

notas.csv

6. Como Executar

Certifique-se de ter o Python 3 instalado.

Execute o arquivo principal:

python main.py


Utilize o menu principal para navegar entre as funcionalidades do sistema.

7. Requisitos Técnicos

Python 3.x

Biblioteca padrão do Python (sqlite3, os, csv, re)

Persistência em SQLite

Estrutura modular

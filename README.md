***** Sistema de Cadastro Escolar (Python + Tkinter + SQLite) *****

Este projeto foi desenvolvido como parte do Trabalho de Desenvolvimento Rápido de Aplicações em Python, conforme os requisitos definidos no documento da disciplina.
O sistema realiza o cadastro, edição, listagem e exclusão de Alunos, Disciplinas e Notas, com persistência de dados em SQLite e exportação em JSON, CSV e TXT.

-- Funcionalidades --

*Cadastro de Alunos

Adicionar, editar e excluir alunos

Validação automática da matrícula (12 dígitos)

Exibição em tabela (TreeView)

*Cadastro de Disciplinas

Adicionar, editar e excluir disciplinas

Campos: nome, turno, sala e professor

Interface simples e intuitiva

*Cadastro de Notas

Atribuir notas aos alunos por disciplina

Permite edição e exclusão de notas

Validação de intervalo (0 a 10)

*Exportações

Exportar todos os dados do sistema para:

CSV (arquivos separados)

-- Estrutura de Arquivos --
projeto_python/
│
├── main.py                     # Janela principal (menu e exportações)
├── cadastrar_alunos.py         # Interface de alunos
├── cadastrar_disciplinas.py    # Interface de disciplinas
├── cadastrar_notas.py          # Interface de notas
├── funcoes.py                  # Funções utilitárias e banco de dados
├── requirements.txt            # Dependências (nenhuma externa)
└── banco_de_dados/
    └── banco_escolar.db        # Criado automaticamente ao rodar o sistema

-- Requisitos --

Python 3.8 ou superior

Nenhuma biblioteca externa necessária
(todas as dependências são nativas do Python)

-- requirements.txt --

# Nenhuma biblioteca externa necessária.
# Todas as dependências são nativas do Python (tkinter, sqlite3, etc.)

-- Como Executar --

Baixe ou clone este repositório:

acesse https://github.com/gugasmhm/projeto_python e baixe o projeto

OBS.: Certifique-se de ter o Python instalado:
python 3.8


Execute o sistema:
python main.py


A janela principal do sistema será aberta com as opções:
"Cadastro de Alunos"

"Cadastro de Disciplinas"

"Cadastro de Notas"

"Exportar CSV"

-- Banco de Dados --

O banco SQLite é criado automaticamente no diretório:

banco_de_dados/banco_escolar.db


As tabelas são geradas na primeira execução, conforme o modelo lógico:

Tabela	Campos Principais
alunos	id, nome, matrícula, data_nascimento
disciplinas	id, nome, turno, sala, professor
notas	id, aluno_id, disciplina_id, nota (0–10)

-- Exportação de Dados --

Os arquivos exportados são salvos automaticamente na pasta:

exportacoes/
│
├── alunos.csv
├── disciplinas.csv
└── notas.csv

-- Tecnologias Utilizadas --
Tecnologia	Função
Python 3	Linguagem principal
Tkinter	Interface gráfica (GUI)
SQLite3	Banco de dados local
CSV	Exportação de dados

-- Autor --

Luiz Maia
Trabalho acadêmico – Estácio de Sá
Disciplina: Desenvolvimento Rápido de Aplicações em Python

-- Licença --

Este projeto é de uso educacional e pode ser reutilizado para fins acadêmicos.
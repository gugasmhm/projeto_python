import sqlite3
import os
import re
import csv

DB_PATH = "banco_de_dados/banco_escolar.db"


# ----------------- UTILIDADES -----------------

def limpar_tela():
    """Limpa a tela."""
    os.system("cls" if os.name == "nt" else "clear")


def conectar():
    """Conecta ao SQLite e cria tabelas se necessário."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    criar_tabelas(conn)
    return conn


def criar_tabelas(conn):
    """Cria todas as tabelas caso ainda não existam."""
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            data_nascimento TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT,
            sala TEXT,
            professor TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10),
            FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
        );
    """)

    conn.commit()


def executar_query(query, params=(), fetchone=False, fetchall=False):
    """Executa comando SQL genérico e controla retorno."""
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        conn.commit()

        if fetchone:
            return cur.fetchone()

        if fetchall:
            return cur.fetchall()

        return cur.lastrowid

    except sqlite3.IntegrityError as e:
        raise e
    finally:
        conn.close()


# ----------------- VALIDAÇÕES -----------------

def validar_matricula(prompt="Digite a matrícula (12 dígitos): "):
    """Valida matrícula com 12 números."""
    padrao = re.compile(r"^\d{12}$")
    while True:
        matricula = input(prompt).strip()
        if padrao.match(matricula):
            return matricula
        print("Matrícula inválida! Digite exatamente 12 números.\n")


# ----------------- FUNÇÕES DE BUSCA -----------------

def obter_aluno_por_matricula(matricula):
    return executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (matricula,),
        fetchone=True,
    )


def obter_aluno_por_id(aluno_id):
    return executar_query(
        "SELECT * FROM alunos WHERE id = ?",
        (aluno_id,),
        fetchone=True,
    )


def listar_alunos_todos():
    rows = executar_query(
        "SELECT * FROM alunos ORDER BY nome",
        fetchall=True
    )
    return rows or []


def listar_disciplinas_todas():
    rows = executar_query(
        "SELECT * FROM disciplinas ORDER BY nome",
        fetchall=True
    )
    return rows or []


def obter_disciplina_por_id(disc_id):
    return executar_query(
        "SELECT * FROM disciplinas WHERE id = ?",
        (disc_id,),
        fetchone=True,
    )


# ----------------- EXPORTAR CSV -----------------

def exportar_csv(nome_arquivo, colunas, dados):
    """
    Exporta qualquer tabela para CSV.
    nome_arquivo = ex: 'alunos.csv'
    colunas = lista de nomes
    dados = lista de sqlite3.Row
    """
    os.makedirs("exportacoes", exist_ok=True)
    caminho = os.path.join("exportacoes", nome_arquivo)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colunas)

        for row in dados:
            writer.writerow([row[c] for c in colunas])

    print(f"\nArquivo exportado com sucesso: {caminho}")
    return caminho


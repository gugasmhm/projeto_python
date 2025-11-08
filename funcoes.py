import sqlite3
import os
import re
import csv
from datetime import datetime

DB_PATH = "banco_de_dados/banco_escolar.db"

# Cria pasta de banco se necessario e retorna conexao com sqlite3.
def conectar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    criar_tabelas(conn)
    return conn


# Cria tabelas basicas se nao existirem.
def criar_tabelas(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            data_nascimento TEXT
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT,
            sala TEXT,
            professor TEXT
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10),
            FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
            FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def executar_query(query, params=(), fetchone=False, fetchall=False):
    """
    Executa INSERT/UPDATE/DELETE/SELECT simplificado.
    Retorna o resultado quando fetchone/fetchall são usados.
    """
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
        # repropaga para o chamador
        raise
    finally:
        conn.close()

# Valida matricula recebida deve ser exatamente 12 digitos.
def validar_matricula_string(matricula_str):
    if matricula_str is None:
        return False
    padrao = re.compile(r"^\d{12}$")
    return bool(padrao.match(matricula_str.strip()))


# ---------- Helpers para menus e buscas ----------
def obter_aluno_por_matricula(matricula):
    row = executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (matricula,),
        fetchone=True,
    )
    return row


def listar_alunos_todos():
    rows = executar_query("SELECT * FROM alunos ORDER BY nome", fetchall=True)
    return rows or []


def listar_disciplinas_todas():
    rows = executar_query("SELECT * FROM disciplinas ORDER BY nome", fetchall=True)
    return rows or []


def obter_disciplina_por_id(disc_id):
    return executar_query(
        "SELECT * FROM disciplinas WHERE id = ?",
        (disc_id,),
        fetchone=True,
    )


def obter_aluno_por_id(aluno_id):
    return executar_query(
        "SELECT * FROM alunos WHERE id = ?",
        (aluno_id,),
        fetchone=True,
    )


# ---------- Exportacoe CSV ----------
def exportar_dados_csv(folder=None):
    folder = folder or "exportacoes"
    os.makedirs(folder, exist_ok=True)

    alunos = [dict(r) for r in listar_alunos_todos()]
    disciplinas = [dict(r) for r in listar_disciplinas_todas()]
    notas = [dict(r) for r in executar_query("SELECT * FROM notas", fetchall=True) or []]

    path_alunos = os.path.join(folder, "alunos.csv")
    with open(path_alunos, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nome", "matricula", "data_nascimento"])
        writer.writeheader()
        for a in alunos:
            writer.writerow(a)

    path_disciplinas = os.path.join(folder, "disciplinas.csv")
    with open(path_disciplinas, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nome", "turno", "sala", "professor"])
        writer.writeheader()
        for d in disciplinas:
            writer.writerow(d)

    path_notas = os.path.join(folder, "notas.csv")
    with open(path_notas, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "aluno_id", "disciplina_id", "nota"])
        writer.writeheader()
        for n in notas:
            writer.writerow(n)

    return (path_alunos, path_disciplinas, path_notas)

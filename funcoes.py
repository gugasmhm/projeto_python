import csv
from datetime import datetime
import os

# ------------------- Funções Auxiliares -------------------
def limpar_tela():
    """Limpa a tela (compatível com Windows, Linux e macOS)"""
    os.system("cls" if os.name == "nt" else "clear")

# ------------------- Funções de Arquivo -------------------
def carregar_dados():
    """Carrega os cadastros do arquivo CSV, se existir"""
    global alunos
    if os.path.exists(ARQUIVO_CSV):
        with open(ARQUIVO_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            alunos = list(reader)
            

def salvar_dados():
    """Salva os cadastros em CSV"""
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "matricula", "data_nascimento"])
        writer.writeheader()
        writer.writerows(alunos)

def input_data_nascimento():
    while True:
        data_txt = input("Digite a data de nascimento (DD/MM/AAAA): ").strip()
        try:
            datetime.strptime(data_txt, "%d/%m/%Y")
            return data_txt
        except ValueError:
            print("⚠️ Data inválida. Use o formato DD/MM/AAAA.")

def input_matricula(aluno_atual=None):
    """Solicita matrícula de 12 dígitos e impede duplicidade"""
    while True:
        matricula = input("Digite a matrícula (12 dígitos): ").strip()
        if not matricula.isdigit():
            print("⚠️ A matrícula deve conter apenas números.")
            continue
        if len(matricula) != 12:
            print("⚠️ A matrícula deve ter exatamente 12 dígitos.")
            continue
        if any(a["matricula"] == matricula for a in alunos if a != aluno_atual):
            print("⚠️ Já existe um aluno com essa matrícula. Tente outra.")
            continue
        return matricula
    

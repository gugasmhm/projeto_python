import os

# ------------------- Funções Auxiliares -------------------
def limpar_tela():
    """Limpa a tela (compatível com Windows, Linux e macOS)"""
    os.system("cls" if os.name == "nt" else "clear")

import re

# ------------------- Validador de Matrícula -------------------
def validar_matricula():
    padrao = re.compile(r"^\d{12}$")  # exatamente 12 dígitos
    while True:
        matricula = input("Digite a matrícula (12 dígitos): ").strip()
        if padrao.match(matricula):
            return matricula
        else:
            print("Matrícula inválida! Digite exatamente 12 números.\n")

import os

# ------------------- Funções Auxiliares -------------------
def limpar_tela():
    """Limpa a tela (compatível com Windows, Linux e macOS)"""
    os.system("cls" if os.name == "nt" else "clear")

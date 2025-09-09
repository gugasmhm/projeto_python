import csv
from datetime import datetime
import os

ARQUIVO_CSV = "alunos.csv"
alunos = []


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


# ------------------- Funções de Cadastro -------------------
def cadastrar_aluno():
    limpar_tela()
    print("=== Cadastro de Aluno ===")

    while True:
        nome = input("Digite o nome do aluno: ").strip()
        if nome:
            break
        print("⚠️ O nome não pode ficar em branco.")

    matricula = input_matricula()
    data_nasc = input_data_nascimento()

    aluno = {
        "nome": nome,
        "matricula": matricula,
        "data_nascimento": data_nasc
    }

    alunos.append(aluno)
    salvar_dados()
    print("✅ Aluno cadastrado com sucesso!\n")


def listar_alunos():
    limpar_tela()
    print("=== Lista de Alunos ===")

    if not alunos:
        print("⚠️ Nenhum aluno cadastrado.\n")
        return

    for i, aluno in enumerate(alunos, start=1):
        print(
            f"{i}. Nome: {aluno['nome']} | "
            f"Matrícula: {aluno['matricula']} | "
            f"Data de Nascimento: {aluno['data_nascimento']}"
        )
    print()


def excluir_aluno():
    limpar_tela()
    print("=== Excluir Aluno ===")

    if not alunos:
        print("⚠️ Nenhum aluno cadastrado para excluir.\n")
        return

    matricula = input("Digite a matrícula do aluno a excluir: ").strip()

    for aluno in alunos:
        if aluno["matricula"] == matricula:
            alunos.remove(aluno)
            salvar_dados()
            print(f"🗑️ Aluno com matrícula {matricula} excluído com sucesso!\n")
            return

    print("⚠️ Matrícula não encontrada.\n")


def editar_aluno():
    limpar_tela()
    print("=== Editar Aluno ===")

    if not alunos:
        print("⚠️ Nenhum aluno cadastrado para editar.\n")
        return

    matricula = input("Digite a matrícula do aluno a editar: ").strip()

    for aluno in alunos:
        if aluno["matricula"] == matricula:
            print(f"✏️ Editando aluno: {aluno['nome']}")

            novo_nome = input(f"Novo nome (Enter para manter '{aluno['nome']}'): ").strip()
            if novo_nome:
                aluno["nome"] = novo_nome

            nova_matricula = input(f"Nova matrícula (12 dígitos, Enter para manter '{aluno['matricula']}'): ").strip()
            if nova_matricula:
                if nova_matricula.isdigit() and len(nova_matricula) == 12:
                    if not any(a["matricula"] == nova_matricula for a in alunos if a != aluno):
                        aluno["matricula"] = nova_matricula
                    else:
                        print("⚠️ Já existe um aluno com essa matrícula. Mantendo a original.")
                else:
                    print("⚠️ Matrícula inválida. Mantendo a original.")

            nova_data = input(f"Nova data de nascimento (DD/MM/AAAA) (Enter para manter '{aluno['data_nascimento']}'): ").strip()
            if nova_data:
                try:
                    datetime.strptime(nova_data, "%d/%m/%Y")
                    aluno["data_nascimento"] = nova_data
                except ValueError:
                    print("⚠️ Data inválida. Mantendo a original.")

            salvar_dados()
            print("✅ Dados do aluno atualizados com sucesso!\n")
            return

    print("⚠️ Matrícula não encontrada.\n")


# ------------------- Menu Principal -------------------
def menu():
    carregar_dados()
    while True:
        limpar_tela()
        print("===== MENU =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Editar aluno")
        print("4 - Excluir aluno")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            editar_aluno()
        elif opcao == "4":
            excluir_aluno()
        elif opcao == "5":
            print("Saindo do sistema... 👋")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.\n")

        input("Pressione ENTER para continuar...")  # pausa antes de voltar ao menu


if __name__ == "__main__":
    menu()

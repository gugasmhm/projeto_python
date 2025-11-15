from funcoes import (
    limpar_tela,
    executar_query,
    validar_matricula,
    listar_alunos_todos,
    exportar_csv,
)
import sqlite3


def cadastrar_aluno():
    limpar_tela()
    print("------ Cadastro de alunos -------")

    nome = input("Digite o nome do aluno: ").strip()
    matricula = validar_matricula()
    data_nasc = input("Digite a data de nascimento (opcional): ").strip() or None

    try:
        executar_query(
            "INSERT INTO alunos (nome, matricula, data_nascimento) VALUES (?, ?, ?)",
            (nome, matricula, data_nasc),
        )
        print("\nAluno cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("\nMatrícula já cadastrada. Operação cancelada.")


def listar_alunos():
    limpar_tela()
    print("------ Lista de alunos -------")
    rows = listar_alunos_todos()

    if not rows:
        print("Nenhum aluno cadastrado.")
        return

    for i, a in enumerate(rows, start=1):
        print(f"{i}. Nome: {a['nome']}, Matrícula: {a['matricula']}, Nasc: {a['data_nascimento']}")


def editar_aluno():
    limpar_tela()
    print("------ Editar Aluno -------")

    # Edita usando matrícula
    matricula = validar_matricula("Digite a matrícula do aluno que deseja editar (12 dígitos): ")

    aluno = executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (matricula,),
        fetchone=True,
    )

    if not aluno:
        print("Aluno não encontrado.")
        return

    print(f"\nAluno encontrado: {aluno['nome']} (Matrícula {aluno['matricula']})")

    novo_nome = input(f"Novo nome [{aluno['nome']}]: ").strip() or aluno['nome']
    nova_data = input(
        f"Nova data de nascimento [{aluno['data_nascimento'] or 'vazio'}]: "
    ).strip() or aluno['data_nascimento']

    executar_query(
        "UPDATE alunos SET nome = ?, data_nascimento = ? WHERE matricula = ?",
        (novo_nome, nova_data, matricula),
    )

    print("\nAluno atualizado com sucesso!")


def excluir_aluno():
    limpar_tela()
    print("------ Excluir Aluno -------")

    matricula = validar_matricula("Digite a matrícula do aluno que deseja excluir: ")

    aluno = executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (matricula,),
        fetchone=True,
    )

    if not aluno:
        print("Aluno não encontrado.")
        return

    confirmar = input(
        f"Confirma exclusão de {aluno['nome']} (Matrícula {aluno['matricula']})? [S/N]: "
    ).strip().lower()

    if confirmar != "s":
        print("Operação cancelada.")
        return

    executar_query("DELETE FROM alunos WHERE matricula = ?", (matricula,))
    print("Aluno removido com sucesso.")


def exportar_alunos_csv():
    dados = listar_alunos_todos()
    if not dados:
        print("Nenhum aluno para exportar.")
        return

    colunas = ["id", "nome", "matricula", "data_nascimento"]
    exportar_csv("alunos.csv", colunas, dados)


def menu_alunos():
    while True:
        limpar_tela()
        print("===== MENU Alunos =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Editar aluno")
        print("4 - Excluir aluno")
        print("5 - Exportar CSV")
        print("6 - Voltar")

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
            exportar_alunos_csv()
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")

        input("\nENTER para continuar...")


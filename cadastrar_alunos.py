from funcoes import (
    limpar_tela,
    executar_query,
    validar_matricula,
    listar_alunos_todos,
    conectar,
)
import sqlite3


def cadastrar_aluno():
    limpar_tela()
    print("------ Cadastro de alunos -------")
    nome = input("Digite o nome do Aluno: ").strip()
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
    print("------ Listar alunos -------")
    rows = listar_alunos_todos()
    if not rows:
        print("Nenhum aluno cadastrado ainda.")
        return
    for i, r in enumerate(rows, start=1):
        print(f"{i}. Nome: {r['nome']}, Matrícula: {r['matricula']}, Data de Nascimento: {r['data_nascimento']}")


def editar_aluno():
    limpar_tela()
    print("------ Editar aluno -------")
    matricula = validar_matricula()
    aluno = executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (matricula,),
        fetchone=True,
    )
    if not aluno:
        print("Aluno não encontrado.")
        return
    print(f"Encontrado: {aluno['nome']} ({aluno['matricula']}) - Nasc: {aluno['data_nascimento']}")
    novo_nome = input(f"Novo nome [{aluno['nome']}]: ").strip() or aluno['nome']
    nova_data = input(f"Nova data de nascimento [{aluno['data_nascimento'] or 'vazio'}]: ").strip() or aluno['data_nascimento']

    executar_query(
        "UPDATE alunos SET nome = ?, data_nascimento = ? WHERE matricula = ?",
        (novo_nome, nova_data, matricula),
    )
    print("Aluno atualizado com sucesso.")


def excluir_aluno():
    limpar_tela()
    print("------ Excluir aluno -------")
    matricula = validar_matricula()
    aluno = executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (matricula,),
        fetchone=True,
    )
    if not aluno:
        print("Aluno não encontrado.")
        return
    confirmar = input(f"Confirma exclusão do aluno {aluno['nome']} (matrícula {aluno['matricula']})? [S/N]: ").strip().lower()
    if confirmar != "s":
        print("Operação cancelada.")
        return
    executar_query("DELETE FROM alunos WHERE matricula = ?", (matricula,))
    print("Aluno removido com sucesso.")


def menu_alunos():
    while True:
        limpar_tela()
        print("===== MENU Alunos =====")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Editar aluno")
        print("4 - Excluir aluno")
        print("5 - Voltar")
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
            break
        else:
            print("Opção inválida! Tente novamente.\n")
        input("\nENTER para continuar...")


from funcoes import (
    limpar_tela,
    executar_query,
    listar_disciplinas_todas,
    exportar_csv
)
import sqlite3


def cadastrar_disciplina():
    limpar_tela()
    print("------ Cadastro de disciplinas -------")

    nome = input("Nome da disciplina: ").strip()
    turno = input("Turno (Manhã/Tarde/Noite) (opcional): ").strip() or None
    sala = input("Sala (opcional): ").strip() or None
    professor = input("Professor (opcional): ").strip() or None

    try:
        executar_query(
            "INSERT INTO disciplinas (nome, turno, sala, professor) VALUES (?, ?, ?, ?)",
            (nome, turno, sala, professor),
        )
        print("\nDisciplina cadastrada com sucesso!")
    except sqlite3.Error:
        print("\nErro ao cadastrar disciplina.")


def listar_disciplina():
    limpar_tela()
    print("------ Lista de disciplinas -------")

    rows = listar_disciplinas_todas()
    if not rows:
        print("Nenhuma disciplina cadastrada.")
        return

    for d in rows:
        print(f"{d['id']}. {d['nome']} | Turno: {d['turno']} | Sala: {d['sala']} | Professor: {d['professor']}")


def editar_disciplina():
    listar_disciplina()

    try:
        disc_id = int(input("ID da disciplina para editar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    disc = executar_query("SELECT * FROM disciplinas WHERE id = ?", (disc_id,), fetchone=True)

    if not disc:
        print("Disciplina não encontrada.")
        return

    novo_nome = input(f"Novo nome [{disc['nome']}]: ").strip() or disc['nome']
    novo_turno = input(f"Novo turno [{disc['turno'] or 'vazio'}]: ").strip() or disc['turno']
    nova_sala = input(f"Nova sala [{disc['sala'] or 'vazio'}]: ").strip() or disc['sala']
    novo_prof = input(f"Novo professor [{disc['professor'] or 'vazio'}]: ").strip() or disc['professor']

    executar_query(
        "UPDATE disciplinas SET nome = ?, turno = ?, sala = ?, professor = ? WHERE id = ?",
        (novo_nome, novo_turno, nova_sala, novo_prof, disc_id),
    )
    print("Disciplina atualizada.")


def excluir_disciplina():
    listar_disciplina()

    try:
        disc_id = int(input("ID da disciplina para excluir: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    disc = executar_query("SELECT * FROM disciplinas WHERE id = ?", (disc_id,), fetchone=True)
    if not disc:
        print("Disciplina não encontrada.")
        return

    confirmar = input(f"Confirma excluir '{disc['nome']}'? [S/N]: ").strip().lower()
    if confirmar != "s":
        print("Operação cancelada.")
        return

    executar_query("DELETE FROM disciplinas WHERE id = ?", (disc_id,))
    print("Disciplina removida.")


def exportar_disciplinas_csv():
    dados = listar_disciplinas_todas()
    if not dados:
        print("Nenhum dado para exportar.")
        return

    colunas = ["id", "nome", "turno", "sala", "professor"]
    exportar_csv("disciplinas.csv", colunas, dados)


def menu_disciplina():
    while True:
        limpar_tela()
        print("===== MENU Disciplinas =====")
        print("1 - Cadastrar disciplina")
        print("2 - Listar disciplinas")
        print("3 - Editar disciplina")
        print("4 - Excluir disciplina")
        print("5 - Exportar CSV")
        print("6 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_disciplina()
        elif opcao == "2":
            listar_disciplina()
        elif opcao == "3":
            editar_disciplina()
        elif opcao == "4":
            excluir_disciplina()
        elif opcao == "5":
            exportar_disciplinas_csv()
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")

        input("\nENTER para continuar...")

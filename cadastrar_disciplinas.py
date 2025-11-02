from funcoes import (
    limpar_tela,
    executar_query,
    listar_disciplinas_todas,
)
import sqlite3


def cadastrar_disciplina():
    limpar_tela()
    print("------ Cadastro de disciplinas -------")
    nome = input("Digite o nome da disciplina: ").strip()
    turno = input("Digite o turno (Manhã/Tarde/Noite) (opcional): ").strip() or None
    sala = input("Digite a sala (opcional): ").strip() or None
    professor = input("Digite o nome do professor (opcional): ").strip() or None

    try:
        executar_query(
            "INSERT INTO disciplinas (nome, turno, sala, professor) VALUES (?, ?, ?, ?)",
            (nome, turno, sala, professor),
        )
        print("\nDisciplina cadastrada com sucesso!")
    except sqlite3.IntegrityError:
        print("\n❌ Erro ao cadastrar disciplina.")


def listar_disciplina():
    limpar_tela()
    print("------ Listar disciplinas -------")
    rows = listar_disciplinas_todas()
    if not rows:
        print("Nenhuma disciplina cadastrada ainda.")
        return
    for r in rows:
        print(f"{r['id']}. Disciplina: {r['nome']}, Turno: {r['turno']}, Sala: {r['sala']}, Professor: {r['professor']}")


def editar_disciplina():
    limpar_tela()
    print("------ Editar disciplina -------")
    listar_disciplina()
    try:
        disc_id = int(input("Digite o ID da disciplina que deseja editar: ").strip())
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
    print("Disciplina atualizada com sucesso.")


def excluir_disciplina():
    limpar_tela()
    print("------ Excluir disciplina -------")
    listar_disciplina()
    try:
        disc_id = int(input("Digite o ID da disciplina que deseja excluir: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    disc = executar_query("SELECT * FROM disciplinas WHERE id = ?", (disc_id,), fetchone=True)
    if not disc:
        print("Disciplina não encontrada.")
        return
    confirmar = input(f"Confirma exclusão da disciplina '{disc['nome']}'? [S/N]: ").strip().lower()
    if confirmar != "s":
        print("Operação cancelada.")
        return
    executar_query("DELETE FROM disciplinas WHERE id = ?", (disc_id,))
    print("Disciplina removida com sucesso.")


def menu_disciplina():
    while True:
        limpar_tela()
        print("===== MENU Disciplina =====")
        print("1 - Cadastrar disciplina")
        print("2 - Listar disciplina")
        print("3 - Editar disciplina")
        print("4 - Excluir disciplina")
        print("5 - Voltar")
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
            break
        else:
            print("Opção inválida! Tente novamente.\n")
        input("\nENTER para continuar...")

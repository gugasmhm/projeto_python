from funcoes import (
    limpar_tela,
    executar_query,
    listar_alunos_todos,
    listar_disciplinas_todas,
    exportar_csv
)
import sqlite3


def escolher_aluno():
    alunos = listar_alunos_todos()
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return None

    for a in alunos:
        print(f"{a['id']}. {a['nome']} - Matrícula {a['matricula']}")

    try:
        aid = int(input("ID do aluno: ").strip())
    except ValueError:
        print("ID inválido.")
        return None

    aluno = executar_query("SELECT * FROM alunos WHERE id = ?", (aid,), fetchone=True)
    return aluno


def escolher_disciplina():
    disciplinas = listar_disciplinas_todas()
    if not disciplinas:
        print("Nenhuma disciplina cadastrada.")
        return None

    for d in disciplinas:
        print(f"{d['id']}. {d['nome']} (Prof: {d['professor']})")

    try:
        did = int(input("ID da disciplina: ").strip())
    except ValueError:
        print("ID inválido.")
        return None

    disc = executar_query("SELECT * FROM disciplinas WHERE id = ?", (did,), fetchone=True)
    return disc


def cadastrar_nota():
    limpar_tela()
    print("------ Cadastro de notas -------")

    aluno = escolher_aluno()
    if not aluno:
        return

    disciplina = escolher_disciplina()
    if not disciplina:
        return

    try:
        nota = float(input("Nota (0 a 10): ").strip())
    except ValueError:
        print("Nota inválida.")
        return

    if not (0 <= nota <= 10):
        print("Nota fora do intervalo permitido.")
        return

    executar_query(
        "INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)",
        (aluno['id'], disciplina['id'], nota),
    )
    print("Nota cadastrada com sucesso.")


def listar_notas():
    limpar_tela()
    print("------ Lista de notas -------")

    rows = executar_query("""
        SELECT n.id, a.nome AS aluno, a.matricula,
               d.nome AS disciplina, d.professor, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        ORDER BY a.nome
    """, fetchall=True)

    if not rows:
        print("Nenhuma nota cadastrada.")
        return

    for n in rows:
        print(f"{n['id']}. Aluno: {n['aluno']} ({n['matricula']}) | Disciplina: {n['disciplina']} | Nota: {n['nota']}")


def editar_nota():
    listar_notas()

    try:
        nid = int(input("ID da nota para editar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    nota_row = executar_query("SELECT * FROM notas WHERE id = ?", (nid,), fetchone=True)

    if not nota_row:
        print("Nota não encontrada.")
        return

    try:
        nova_nota = float(input(f"Nova nota (0-10) [{nota_row['nota']}]: ").strip() or nota_row['nota'])
    except ValueError:
        print("Valor inválido.")
        return

    if not (0 <= nova_nota <= 10):
        print("Nota fora do intervalo.")
        return

    executar_query("UPDATE notas SET nota = ? WHERE id = ?", (nova_nota, nid))
    print("Nota atualizada.")


def excluir_nota():
    listar_notas()

    try:
        nid = int(input("ID da nota para excluir: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    nota = executar_query("""
        SELECT n.id, a.nome AS aluno, d.nome AS disciplina, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        WHERE n.id = ?
    """, (nid,), fetchone=True)

    if not nota:
        print("Nota não encontrada.")
        return

    confirmar = input(f"Excluir nota {nota['id']} de {nota['aluno']} - {nota['disciplina']}? [S/N]: ").strip().lower()
    if confirmar != "s":
        print("Operação cancelada.")
        return

    executar_query("DELETE FROM notas WHERE id = ?", (nid,))
    print("Nota removida.")


def exportar_notas_csv():
    rows = executar_query("""
        SELECT n.id, a.nome AS aluno, a.matricula,
               d.nome AS disciplina, d.professor, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
    """, fetchall=True)

    if not rows:
        print("Nada para exportar.")
        return

    colunas = ["id", "aluno", "matricula", "disciplina", "professor", "nota"]
    exportar_csv("notas.csv", colunas, rows)


def menu_notas():
    while True:
        limpar_tela()
        print("===== MENU Notas =====")
        print("1 - Cadastrar nota")
        print("2 - Listar notas")
        print("3 - Editar nota")
        print("4 - Excluir nota")
        print("5 - Exportar CSV")
        print("6 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_nota()
        elif opcao == "2":
            listar_notas()
        elif opcao == "3":
            editar_nota()
        elif opcao == "4":
            excluir_nota()
        elif opcao == "5":
            exportar_notas_csv()
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")

        input("\nENTER para continuar...")

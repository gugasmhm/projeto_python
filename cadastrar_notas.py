from funcoes import (
    limpar_tela,
    executar_query,
    listar_disciplinas_todas,
    exportar_csv
)
import sqlite3


# -------------------------------------------------------------
# Selecionar aluno APENAS pela matrícula
# -------------------------------------------------------------
def escolher_aluno_por_matricula():
    print("------ Selecionar Aluno pela Matrícula ------")
    mat = input("Digite a matrícula do aluno (12 dígitos): ").strip()

    aluno = executar_query(
        "SELECT * FROM alunos WHERE matricula = ?",
        (mat,),
        fetchone=True
    )

    if not aluno:
        print("Aluno não encontrado. Verifique a matrícula.")
        return None

    print(f"Aluno encontrado: {aluno['nome']} (Matrícula {aluno['matricula']})")
    return aluno


# -------------------------------------------------------------
# Listar disciplinas e escolher diretamente pelo ID
# -------------------------------------------------------------
def escolher_disciplina_por_id():
    print("------ Selecionar Disciplina -------")

    disciplinas = listar_disciplinas_todas()
    if not disciplinas:
        print("Nenhuma disciplina cadastrada.")
        return None

    print("\nDisciplinas cadastradas:")
    for d in disciplinas:
        print(f"{d['id']}. {d['nome']} | Professor: {d['professor']} | Sala: {d['sala']}")

    try:
        did = int(input("\nDigite o ID da disciplina desejada: ").strip())
    except ValueError:
        print("ID inválido.")
        return None

    disc = executar_query(
        "SELECT * FROM disciplinas WHERE id = ?",
        (did,),
        fetchone=True
    )

    if not disc:
        print("Disciplina não encontrada.")
        return None

    return disc


# -------------------------------------------------------------
# Cadastrar Nota
# -------------------------------------------------------------
def cadastrar_nota():
    limpar_tela()
    print("------ Cadastro de Notas (por matrícula) -------")

    aluno = escolher_aluno_por_matricula()
    if not aluno:
        return

    disciplina = escolher_disciplina_por_id()
    if not disciplina:
        return

    try:
        nota = float(input("Digite a nota (0 a 10): ").strip())
    except ValueError:
        print("Valor de nota inválido.")
        return

    if nota < 0 or nota > 10:
        print("Nota fora do intervalo permitido.")
        return

    try:
        executar_query(
            "INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)",
            (aluno["id"], disciplina["id"], nota),
        )
        print("Nota cadastrada com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro ao cadastrar nota.")


# -------------------------------------------------------------
# Listar Notas
# -------------------------------------------------------------
def listar_notas():
    limpar_tela()
    print("------ Listar Notas -------")

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

    for r in rows:
        print(f"{r['id']}. Aluno: {r['aluno']} ({r['matricula']}) | "
              f"Disciplina: {r['disciplina']} | Nota: {r['nota']}")


# -------------------------------------------------------------
# Editar Nota
# -------------------------------------------------------------
def editar_nota():
    listar_notas()

    try:
        nid = int(input("\nDigite o ID da nota para editar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    nota_row = executar_query(
        "SELECT * FROM notas WHERE id = ?",
        (nid,),
        fetchone=True
    )

    if not nota_row:
        print("Nota não encontrada.")
        return

    try:
        nova_nota = float(
            input(f"Nova nota (0-10) [{nota_row['nota']}]: ").strip() or nota_row["nota"]
        )
    except ValueError:
        print("Valor inválido.")
        return

    if nova_nota < 0 or nova_nota > 10:
        print("Nota fora do intervalo permitido.")
        return

    executar_query(
        "UPDATE notas SET nota = ? WHERE id = ?",
        (nova_nota, nid)
    )
    print("Nota atualizada com sucesso.")


# -------------------------------------------------------------
# Excluir Nota
# -------------------------------------------------------------
def excluir_nota():
    listar_notas()

    try:
        nid = int(input("\nDigite o ID da nota que deseja excluir: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    nota_row = executar_query("""
        SELECT n.id, a.nome AS aluno, d.nome AS disciplina, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        WHERE n.id = ?
    """, (nid,), fetchone=True)

    if not nota_row:
        print("Nota não encontrada.")
        return

    confirmar = input(
        f"Confirma exclusão da nota {nota_row['id']} "
        f"do aluno {nota_row['aluno']} na disciplina {nota_row['disciplina']}? [S/N]: "
    ).strip().lower()

    if confirmar != "s":
        print("Operação cancelada.")
        return

    executar_query("DELETE FROM notas WHERE id = ?", (nid,))
    print("Nota removida com sucesso.")


# -------------------------------------------------------------
# Exportar CSV
# -------------------------------------------------------------
def exportar_notas_csv():
    rows = executar_query("""
        SELECT n.id, a.nome AS aluno, a.matricula,
               d.nome AS disciplina, d.professor, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
    """, fetchall=True)

    if not rows:
        print("Nenhuma nota para exportar.")
        return

    colunas = ["id", "aluno", "matricula", "disciplina", "professor", "nota"]
    exportar_csv("notas.csv", colunas, rows)


# -------------------------------------------------------------
# Menu
# -------------------------------------------------------------
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

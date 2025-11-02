from funcoes import (
    limpar_tela,
    executar_query,
    listar_alunos_todos,
    listar_disciplinas_todas,
    obter_aluno_por_id,
    obter_disciplina_por_id,
)
import sqlite3


def escolher_aluno():
    alunos = listar_alunos_todos()
    if not alunos:
        print("Nenhum aluno cadastrado. Cadastre alunos antes.")
        return None
    for a in alunos:
        print(f"{a['id']}. {a['nome']} (Matrícula: {a['matricula']})")
    try:
        aid = int(input("Digite o ID do aluno: ").strip())
    except ValueError:
        print("ID inválido.")
        return None
    aluno = executar_query("SELECT * FROM alunos WHERE id = ?", (aid,), fetchone=True)
    if not aluno:
        print("Aluno não encontrado.")
        return None
    return aluno


def escolher_disciplina():
    disciplinas = listar_disciplinas_todas()
    if not disciplinas:
        print("Nenhuma disciplina cadastrada. Cadastre disciplinas antes.")
        return None
    for d in disciplinas:
        print(f"{d['id']}. {d['nome']} (Prof: {d['professor']})")
    try:
        did = int(input("Digite o ID da disciplina: ").strip())
    except ValueError:
        print("ID inválido.")
        return None
    disc = executar_query("SELECT * FROM disciplinas WHERE id = ?", (did,), fetchone=True)
    if not disc:
        print("Disciplina não encontrada.")
        return None
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
        nota = float(input("Digite a nota (0 a 10): ").strip())
    except ValueError:
        print("Valor de nota inválido.")
        return
    if nota < 0 or nota > 10:
        print("Nota fora do intervalo permitido (0-10).")
        return
    try:
        executar_query(
            "INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)",
            (aluno['id'], disciplina['id'], nota),
        )
        print("Nota cadastrada com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro ao cadastrar nota.")


def listar_notas():
    limpar_tela()
    print("------ Listar notas -------")
    rows = executar_query(
        """
        SELECT n.id, a.nome AS aluno, a.matricula, d.nome AS disciplina, d.professor, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        ORDER BY a.nome
        """,
        fetchall=True,
    )
    if not rows:
        print("Nenhuma nota cadastrada ainda.")
        return
    for r in rows:
        print(f"{r['id']}. Aluno: {r['aluno']} ({r['matricula']}) | Disciplina: {r['disciplina']} (Prof: {r['professor']}) | Nota: {r['nota']}")


def editar_nota():
    limpar_tela()
    print("------ Editar nota -------")
    listar_notas()
    try:
        nid = int(input("Digite o ID da nota que deseja editar: ").strip())
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
    if nova_nota < 0 or nova_nota > 10:
        print("Nota fora do intervalo permitido (0-10).")
        return
    executar_query("UPDATE notas SET nota = ? WHERE id = ?", (nova_nota, nid))
    print("Nota atualizada com sucesso.")


def excluir_nota():
    limpar_tela()
    print("------ Excluir nota -------")
    listar_notas()
    try:
        nid = int(input("Digite o ID da nota que deseja excluir: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    nota_row = executar_query("SELECT n.id, a.nome AS aluno, d.nome AS disciplina, n.nota FROM notas n JOIN alunos a ON n.aluno_id=a.id JOIN disciplinas d ON n.disciplina_id=d.id WHERE n.id = ?", (nid,), fetchone=True)
    if not nota_row:
        print("Nota não encontrada.")
        return
    confirmar = input(f"Confirma exclusão da nota {nota_row['id']} - Aluno: {nota_row['aluno']} / Disciplina: {nota_row['disciplina']} / Nota: {nota_row['nota']} ? [S/N]: ").strip().lower()
    if confirmar != "s":
        print("Operação cancelada.")
        return
    executar_query("DELETE FROM notas WHERE id = ?", (nid,))
    print("Nota removida com sucesso.")


def menu_notas():
    while True:
        limpar_tela()
        print("===== MENU Notas =====")
        print("1 - Cadastrar nota")
        print("2 - Listar notas")
        print("3 - Editar nota")
        print("4 - Excluir nota")
        print("5 - Voltar")
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
            break
        else:
            print("Opção inválida! Tente novamente.\n")
        input("\nENTER para continuar...")

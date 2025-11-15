from funcoes import (
    limpar_tela,
    executar_query,
)
    

def consultar_por_matricula():
    limpar_tela()
    print("------ Consultar Notas por Matrícula ------")

    mat = input("Digite a matrícula (12 dígitos): ").strip()

    rows = executar_query("""
        SELECT a.nome AS aluno, a.matricula, d.nome AS disciplina, d.professor, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        WHERE a.matricula = ?
        ORDER BY d.nome
    """, (mat,), fetchall=True)

    if not rows:
        print("Nenhuma nota encontrada para esta matrícula.")
        return

    print(f"\nNotas do aluno ({rows[0]['matricula']}): {rows[0]['aluno']}\n")
    for r in rows:
        print(f"Disciplina: {r['disciplina']} | Professor: {r['professor']} | Nota: {r['nota']}")


def consultar_por_nome():
    limpar_tela()
    print("------ Consultar Notas por Nome ------")

    nome = input("Digite parte do nome do aluno: ").strip()

    rows = executar_query("""
        SELECT a.nome AS aluno, a.matricula, d.nome AS disciplina, d.professor, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        WHERE a.nome LIKE ?
        ORDER BY a.nome, d.nome
    """, (f"%{nome}%",), fetchall=True)

    if not rows:
        print("Nenhuma nota encontrada para este nome.")
        return

    print("")
    for r in rows:
        print(f"Aluno: {r['aluno']} ({r['matricula']}) | {r['disciplina']} | Nota: {r['nota']}")


def consultar_por_disciplina():
    limpar_tela()
    print("------ Consultar Notas por Disciplina ------")

    disc = input("Digite parte do nome da disciplina: ").strip()

    rows = executar_query("""
        SELECT d.nome AS disciplina, a.nome AS aluno, a.matricula, n.nota
        FROM notas n
        JOIN alunos a ON n.aluno_id = a.id
        JOIN disciplinas d ON n.disciplina_id = d.id
        WHERE d.nome LIKE ?
        ORDER BY d.nome, a.nome
    """, (f"%{disc}%",), fetchall=True)

    if not rows:
        print("Nenhuma nota encontrada para esta disciplina.")
        return

    print("")
    for r in rows:
        print(f"Disciplina: {r['disciplina']} | Aluno: {r['aluno']} ({r['matricula']}) | Nota: {r['nota']}")


def listar_todas():
    limpar_tela()
    print("------ Todas as Notas ------")

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
        print(f"{r['id']} - {r['aluno']} ({r['matricula']}) | {r['disciplina']} | Nota: {r['nota']}")


def consultar_nota():
    while True:
        limpar_tela()
        print("===== CONSULTA DE NOTAS =====")
        print("1 - Consultar por Matrícula")
        print("2 - Consultar por Nome do Aluno")
        print("3 - Consultar por Disciplina")
        print("4 - Listar Todas as Notas")
        print("5 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            consultar_por_matricula()
        elif opcao == "2":
            consultar_por_nome()
        elif opcao == "3":
            consultar_por_disciplina()
        elif opcao == "4":
            listar_todas()
        elif opcao == "5":
            break
        else:
            print("Opção inválida!")

        input("\nENTER para continuar...")

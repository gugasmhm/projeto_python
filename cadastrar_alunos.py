import os
alunos = []

# ------------------- Cadastro de alunos -------------------
def cadastrar_aluno():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de alunos -------")

    nome = input("Digite o nome do Aluno: ")
    matricula = input("Digite a matrícula: ")
    data_nasc = input("Digite a data de nascimento: ")

    aluno = {"Nome": nome, "Matrícula": matricula, "Data de Nascimento": data_nasc}

    alunos.append(aluno)
    os.makedirs("banco_de_dados", exist_ok=True)

    with open("banco_de_dados/alunos.txt", "a", encoding="utf-8") as f:
        f.write(f"{nome};{matricula};{data_nasc}\n")

    print("\n Aluno cadastrado com sucesso!")
    return aluno


# ------------------- Listar alunos -------------------
def listar_alunos():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Listar alunos -------")

    try:
        with open("banco_de_dados/alunos.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("Nenhum aluno cadastrado ainda.")
        return

    if not linhas:
        print("Nenhum aluno cadastrado ainda.")
    else:
        for i, linha in enumerate(linhas, start=1):
            nome, matricula, data_nasc = linha.strip().split(";")
            print(f"{i}. Aluno: {nome}, Matrícula: {matricula}, Data de Nascimento: {data_nasc}")


# ------------------- Editar alunos -------------------
def editar_aluno():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de alunos -------")
    print("W.I.P.")


# ------------------- Excluir de alunos -------------------
def excluir_aluno():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Excluir de alunos -------")
    print("W.I.P.")


# ------------------- Menu Alunos -------------------
def menu_alunos():
    while True:
        from funcoes import limpar_tela
        limpar_tela()
        print("===== MENU Alunos=====")
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
            input("ENTER para continuar...")
            continue

        input("\nENTER para voltar ao menu de alunos...")

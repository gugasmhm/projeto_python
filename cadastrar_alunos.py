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
    print("\n Aluno cadastrado com sucesso!")

# ------------------- Listar alunos -------------------
def listar_alunos():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Listar alunos -------")

    if not alunos:
        print("Nenhum Aluno cadastrado ainda.")
    else:
        for i, d in enumerate(alunos, start=1):
            print(f"{i}. Aluno: {d['Nome']}, Matrícula: {d['Matrícula']}, Data de Nascimento: {d['Data de Nascimento']}")

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
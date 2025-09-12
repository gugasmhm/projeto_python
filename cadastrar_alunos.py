# ------------------- Cadastro de Alunos -------------------
def cadastrar_aluno():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de Alunos -------")
    nome = input("Digite o nome do aluno: ")
    print(nome)

# ------------------- Listar Alunos -------------------
def listar_alunos():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Listar Alunos -------")
    print("W.I.P.")

# ------------------- Editar Alunos -------------------
def editar_aluno():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de Alunos -------")
    print("W.I.P.")

# ------------------- Excluir de Alunos -------------------
def excluir_aluno():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Excluir de Alunos -------")
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
            print("⚠️ Opção inválida! Tente novamente.\n")
            input("ENTER para continuar...")
            continue

        input("\nENTER para voltar ao menu de alunos...")
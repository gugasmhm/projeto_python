# ------------------- Cadastro de notas -------------------
def cadastrar_nota():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de notas -------")
    val_nota = input("Digite a Nota: ")
    print(val_nota)

# ------------------- Editar notas -------------------
def editar_nota():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de notas -------")
    print("W.I.P.")

# ------------------- Excluir de notas -------------------
def excluir_nota():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Excluir de notas -------")
    print("W.I.P.")


# ------------------- Menu notas -------------------
def menu_notas():
    while True:
        from funcoes import limpar_tela
        limpar_tela()
        print("===== MENU Notas =====")
        print("1 - Cadastrar nota")
        print("3 - Editar nota")
        print("3 - Excluir nota")
        print("4 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_nota()
        elif opcao == "2":
            editar_nota()
        elif opcao == "3":
            excluir_nota()
        elif opcao == "4":
            break
        else:
            print("Opção inválida! Tente novamente.\n")
            input("ENTER para continuar...")
            continue


        input("\nENTER para voltar ao menu de notas...")


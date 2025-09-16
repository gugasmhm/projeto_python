import os
disciplinas = []

# ------------------- Cadastro de disciplinas -------------------
def cadastrar_disciplina():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de disciplinas -------")

    nome = input("Digite o nome da disciplina: ")
    turno = input("Digite o turno (Manhã/Tarde/Noite): ")
    sala = input("Digite a sala: ")
    professor = input("Digite o nome do professor: ")

    disciplina = {"Nome": nome, "Turno": turno, "Sala": sala, "Professor": professor}

    disciplinas.append(disciplina)
    os.makedirs("banco_de_dados", exist_ok=True)

    with open("banco_de_dados/disciplinas.txt", "a", encoding="utf-8") as f:
        f.write(f"{nome};{turno};{sala};{professor}\n")

    print("\nDisciplina cadastrada com sucesso!")
    return disciplina


# ------------------- Listar disciplinas -------------------
def listar_disciplina():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Listar disciplinas -------")

    try:
        with open("banco_de_dados/disciplinas.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("Nenhuma disciplina cadastrada ainda.")
        return

    if not linhas:
        print("Nenhuma disciplina cadastrada ainda.")
    else:
        for i, linha in enumerate(linhas, start=1):
            nome, turno, sala, professor = linha.strip().split(";")
            print(f"{i}. Disciplina: {nome}, Turno: {turno}, Sala: {sala}, Professor: {professor}")


# ------------------- Editar disciplinas -------------------
def editar_disciplina():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Cadastro de disciplinas -------")
    print("W.I.P.")

# ------------------- Excluir de disciplinas -------------------
def excluir_disciplina():
    from funcoes import limpar_tela
    limpar_tela()
    print("------ Excluir de disciplinas -------")
    print("W.I.P.")

# ------------------- Menu disciplinas -------------------
def menu_disciplina():
    while True:
        from funcoes import limpar_tela
        limpar_tela()
        print("===== MENU Disciplina=====")
        print("1 - Cadastrar disciplina")
        print("2 - Listar disciplina")
        print("3 - Editar disciplina")
        print("4 - Excluir disciplina")
        print("5 - Voltar")

        opcao = input("Escolha uma opção: ")

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
            input("ENTER para continuar...")
            continue

        input("\nENTER para voltar ao menu de disciplinas...")
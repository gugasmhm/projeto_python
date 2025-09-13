# ------------------- Menu Principal -------------------
def menu():
    while True:
        from funcoes import limpar_tela
        limpar_tela()
        print(f"{'  =@@@@@@*          *@:     =@-           -@@-         ':^80}")
        print(f"{' +@#:      =*****+:*%@#* :******   :+**** :++:  +*#*+: ':^80}")
        print(f"{' %@@@@@@@*-@%:      *@:        @@ -@#:    -@@- @@:  *@=':^80}")
        print(f"{' +@#-      :+***@%  *@:  =@%***@@ -@*     -@@- @@   *@+':^80}")
        print(f"{'  -%@@@@@+-%@@@@@*  =@@@ -@@@@@@@  =%@@@@ -@@- -@@@@@= ':^80}")
        print("")
        print("===== MENU Principal =====")
        print("1 - Cadastrar Aluno")
        print("2 - Cadastrar Disciplinas")
        print("3 - Cadastrar Notas")
        print("4 - Consulta Notas")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            from cadastrar_alunos import menu_alunos
            menu_alunos()
        elif opcao == "2":
            from cadastrar_disciplinas import menu_disciplina
            menu_disciplina()
        elif opcao == "3":
            from cadastrar_notas import menu_notas
            menu_notas()         
        elif opcao == "4":
            from consultar_notas import consultar_nota
            consultar_nota()
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.\n")

        input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    menu()
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from funcoes import executar_query, listar_alunos_todos, obter_aluno_por_id, validar_matricula_string
import sqlite3


def abrir_tela_alunos(parent):
    win = tk.Toplevel(parent)
    win.title("Menu Alunos")
    win.geometry("640x420")
    win.transient(parent)

    frame = ttk.Frame(win, padding=8)
    frame.pack(fill="both", expand=True)

    cols = ("id", "nome", "matricula", "data_nascimento")
    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    for c in cols:
        tree.heading(c, text=c.capitalize())
        tree.column(c, anchor="w", width=140 if c != "nome" else 220)
    tree.pack(fill="both", expand=True, side="left")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="left", fill="y")

    def carregar():
        for i in tree.get_children():
            tree.delete(i)
        rows = listar_alunos_todos()
        for r in rows:
            tree.insert("", "end", values=(r["id"], r["nome"], r["matricula"], r["data_nascimento"]))

    def adicionar():
        form = tk.Toplevel(win)
        form.title("Adicionar Aluno")
        form.transient(win)
        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        nome_e = ttk.Entry(form, width=40); nome_e.grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(form, text="Matrícula (12 dígitos):").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        mat_e = ttk.Entry(form, width=20); mat_e.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        ttk.Label(form, text="Data Nascimento:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        data_e = ttk.Entry(form, width=20); data_e.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        def salvar():
            nome = nome_e.get().strip()
            mat = mat_e.get().strip()
            data = data_e.get().strip() or None
            if not nome:
                messagebox.showwarning("Validação", "Nome obrigatório.", parent=form); return
            if not validar_matricula_string(mat):
                messagebox.showwarning("Validação", "Matrícula inválida. Deve ter 12 dígitos.", parent=form); return
            try:
                executar_query("INSERT INTO alunos (nome, matricula, data_nascimento) VALUES (?, ?, ?)", (nome, mat, data))
                messagebox.showinfo("OK", "Aluno cadastrado.", parent=form)
                form.destroy()
                carregar()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Matrícula já cadastrada ou erro no cadastro.", parent=form)

        ttk.Button(form, text="Salvar", command=salvar).grid(row=3, column=0, pady=10, padx=6)
        ttk.Button(form, text="Cancelar", command=form.destroy).grid(row=3, column=1, pady=10, padx=6, sticky="e")

    def editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione um aluno.", parent=win); return
        item = tree.item(sel[0])["values"]
        aid = item[0]
        aluno = obter_aluno_por_id(aid)
        if not aluno:
            messagebox.showerror("Erro", "Aluno não encontrado.", parent=win); return

        form = tk.Toplevel(win)
        form.title("Editar Aluno")
        form.transient(win)
        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        nome_e = ttk.Entry(form, width=40); nome_e.insert(0, aluno["nome"]); nome_e.grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(form, text="Matrícula (12 dígitos):").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        mat_lbl = ttk.Label(form, text=aluno["matricula"]); mat_lbl.grid(row=1, column=1, sticky="w", padx=6, pady=6)
        ttk.Label(form, text="Data Nascimento:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        data_e = ttk.Entry(form, width=20); data_e.insert(0, aluno["data_nascimento"] or ""); data_e.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        def salvar():
            novo_nome = nome_e.get().strip()
            nova_data = data_e.get().strip() or None
            if not novo_nome:
                messagebox.showwarning("Validação", "Nome obrigatório.", parent=form); return
            executar_query("UPDATE alunos SET nome = ?, data_nascimento = ? WHERE id = ?", (novo_nome, nova_data, aid))
            messagebox.showinfo("OK", "Aluno atualizado.", parent=form)
            form.destroy()
            carregar()

        ttk.Button(form, text="Salvar", command=salvar).grid(row=3, column=0, pady=10, padx=6)
        ttk.Button(form, text="Cancelar", command=form.destroy).grid(row=3, column=1, pady=10, padx=6, sticky="e")

    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione um aluno.", parent=win); return
        item = tree.item(sel[0])["values"]
        aid = item[0]; nome = item[1]
        if messagebox.askyesno("Confirma", f"Confirma exclusão de {nome}?", parent=win):
            executar_query("DELETE FROM alunos WHERE id = ?", (aid,))
            messagebox.showinfo("OK", "Aluno excluído.", parent=win)
            carregar()

    # Botões
    btns = ttk.Frame(win, padding=6)
    btns.pack(fill="x")
    ttk.Button(btns, text="Adicionar", command=adicionar).pack(side="left", padx=4)
    ttk.Button(btns, text="Editar", command=editar).pack(side="left", padx=4)
    ttk.Button(btns, text="Excluir", command=excluir).pack(side="left", padx=4)
    ttk.Button(btns, text="Fechar", command=win.destroy).pack(side="right", padx=4)

    carregar()
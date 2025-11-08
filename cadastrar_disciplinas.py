import tkinter as tk
from tkinter import ttk, messagebox
from funcoes import executar_query, listar_disciplinas_todas, obter_disciplina_por_id
import sqlite3


def abrir_tela_disciplinas(parent):
    win = tk.Toplevel(parent)
    win.title("Menu Disciplinas")
    win.geometry("690x420")
    win.transient(parent)

    frame = ttk.Frame(win, padding=8)
    frame.pack(fill="both", expand=True)

    cols = ("id", "nome", "turno", "sala", "professor")
    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    for c in cols:
        tree.heading(c, text=c.capitalize())
        tree.column(c, anchor="w", width=120 if c != "nome" else 220)
    tree.pack(fill="both", expand=True, side="left")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="left", fill="y")

    def carregar():
        for i in tree.get_children():
            tree.delete(i)
        rows = listar_disciplinas_todas()
        for r in rows:
            tree.insert("", "end", values=(r["id"], r["nome"], r["turno"], r["sala"], r["professor"]))

    def adicionar():
        form = tk.Toplevel(win)
        form.title("Adicionar Disciplina")
        form.transient(win)
        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        nome_e = ttk.Entry(form, width=40); nome_e.grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(form, text="Turno (Manhã/Tarde/Noite):").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        turno_e = ttk.Entry(form, width=20); turno_e.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        ttk.Label(form, text="Sala:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        sala_e = ttk.Entry(form, width=20); sala_e.grid(row=2, column=1, padx=6, pady=6, sticky="w")
        ttk.Label(form, text="Professor:").grid(row=3, column=0, sticky="w", padx=6, pady=6)
        prof_e = ttk.Entry(form, width=30); prof_e.grid(row=3, column=1, padx=6, pady=6, sticky="w")

        def salvar():
            nome = nome_e.get().strip()
            turno = turno_e.get().strip() or None
            sala = sala_e.get().strip() or None
            prof = prof_e.get().strip() or None
            if not nome:
                messagebox.showwarning("Validação", "Nome da disciplina obrigatório.", parent=form); return
            try:
                executar_query("INSERT INTO disciplinas (nome, turno, sala, professor) VALUES (?, ?, ?, ?)", (nome, turno, sala, prof))
                messagebox.showinfo("OK", "Disciplina cadastrada.", parent=form)
                form.destroy()
                carregar()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Erro ao cadastrar disciplina.", parent=form)

        ttk.Button(form, text="Salvar", command=salvar).grid(row=4, column=0, pady=10, padx=6)
        ttk.Button(form, text="Cancelar", command=form.destroy).grid(row=4, column=1, pady=10, padx=6, sticky="e")

    def editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione uma disciplina.", parent=win); return
        item = tree.item(sel[0])["values"]
        did = item[0]
        disc = obter_disciplina_por_id(did)
        if not disc:
            messagebox.showerror("Erro", "Disciplina não encontrada.", parent=win); return

        form = tk.Toplevel(win)
        form.title("Editar Disciplina")
        form.transient(win)
        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        nome_e = ttk.Entry(form, width=40); nome_e.insert(0, disc["nome"]); nome_e.grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(form, text="Turno (Manhã/Tarde/Noite):").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        turno_e = ttk.Entry(form, width=20); turno_e.insert(0, disc["turno"] or ""); turno_e.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        ttk.Label(form, text="Sala:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        sala_e = ttk.Entry(form, width=20); sala_e.insert(0, disc["sala"] or ""); sala_e.grid(row=2, column=1, padx=6, pady=6, sticky="w")
        ttk.Label(form, text="Professor:").grid(row=3, column=0, sticky="w", padx=6, pady=6)
        prof_e = ttk.Entry(form, width=30); prof_e.insert(0, disc["professor"] or ""); prof_e.grid(row=3, column=1, padx=6, pady=6, sticky="w")

        def salvar():
            nome = nome_e.get().strip()
            turno = turno_e.get().strip() or None
            sala = sala_e.get().strip() or None
            prof = prof_e.get().strip() or None
            if not nome:
                messagebox.showwarning("Validação", "Nome obrigatório.", parent=form); return
            executar_query("UPDATE disciplinas SET nome = ?, turno = ?, sala = ?, professor = ? WHERE id = ?", (nome, turno, sala, prof, did))
            messagebox.showinfo("OK", "Disciplina atualizada.", parent=form)
            form.destroy()
            carregar()

        ttk.Button(form, text="Salvar", command=salvar).grid(row=4, column=0, pady=10, padx=6)
        ttk.Button(form, text="Cancelar", command=form.destroy).grid(row=4, column=1, pady=10, padx=6, sticky="e")

    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione uma disciplina.", parent=win); return
        item = tree.item(sel[0])["values"]
        did = item[0]; nome = item[1]
        if messagebox.askyesno("Confirma", f"Confirma exclusão de {nome}?", parent=win):
            executar_query("DELETE FROM disciplinas WHERE id = ?", (did,))
            messagebox.showinfo("OK", "Disciplina excluída.", parent=win)
            carregar()

    btns = ttk.Frame(win, padding=6)
    btns.pack(fill="x")
    ttk.Button(btns, text="Adicionar", command=adicionar).pack(side="left", padx=4)
    ttk.Button(btns, text="Editar", command=editar).pack(side="left", padx=4)
    ttk.Button(btns, text="Excluir", command=excluir).pack(side="left", padx=4)
    ttk.Button(btns, text="Fechar", command=win.destroy).pack(side="right", padx=4)

    carregar()
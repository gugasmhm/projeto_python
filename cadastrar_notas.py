import tkinter as tk
from tkinter import ttk, messagebox
from funcoes import (
    executar_query,
    listar_alunos_todos,
    listar_disciplinas_todas,
)
import sqlite3


def abrir_tela_notas(parent):
    win = tk.Toplevel(parent)
    win.title("Menu Notas")
    win.geometry("860x460")
    win.transient(parent)

    frame = ttk.Frame(win, padding=8)
    frame.pack(fill="both", expand=True)

    cols = ("id", "aluno", "matricula", "disciplina", "professor", "nota")
    tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    for c in cols:
        tree.heading(c, text=c.capitalize())
        tree.column(c, anchor="w", width=120 if c not in ("aluno", "disciplina") else 200)
    tree.pack(fill="both", expand=True, side="left")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="left", fill="y")

    def carregar():
        for i in tree.get_children():
            tree.delete(i)
        rows = executar_query(
            """
            SELECT n.id, a.nome AS aluno, a.matricula, d.nome AS disciplina, d.professor, n.nota
            FROM notas n
            JOIN alunos a ON n.aluno_id = a.id
            JOIN disciplinas d ON n.disciplina_id = d.id
            ORDER BY a.nome
            """, fetchall=True
        ) or []
        for r in rows:
            tree.insert("", "end", values=(r["id"], r["aluno"], r["matricula"], r["disciplina"], r["professor"], r["nota"]))

    def adicionar():
        form = tk.Toplevel(win)
        form.title("Adicionar Nota")
        form.transient(win)

        ttk.Label(form, text="Aluno:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        alunos = listar_alunos_todos()
        if not alunos:
            messagebox.showwarning("Aviso", "Cadastre alunos antes.", parent=win); return
        aluno_map = {f"{a['id']} - {a['nome']} ({a['matricula']})": a['id'] for a in alunos}
        aluno_cb = ttk.Combobox(form, values=list(aluno_map.keys()), state="readonly", width=60)
        aluno_cb.grid(row=0, column=1, padx=6, pady=6)
        aluno_cb.current(0)

        ttk.Label(form, text="Disciplina:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        disciplinas = listar_disciplinas_todas()
        if not disciplinas:
            messagebox.showwarning("Aviso", "Cadastre disciplinas antes.", parent=win); return
        disc_map = {f"{d['id']} - {d['nome']} (Prof: {d['professor']})": d['id'] for d in disciplinas}
        disc_cb = ttk.Combobox(form, values=list(disc_map.keys()), state="readonly", width=60)
        disc_cb.grid(row=1, column=1, padx=6, pady=6)
        disc_cb.current(0)

        ttk.Label(form, text="Nota (0-10):").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        nota_e = ttk.Entry(form, width=10); nota_e.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        def salvar():
            aluno_key = aluno_cb.get()
            disc_key = disc_cb.get()
            try:
                nota = float(nota_e.get().strip())
            except Exception:
                messagebox.showerror("Erro", "Nota inválida.", parent=form); return
            if nota < 0 or nota > 10:
                messagebox.showerror("Erro", "Nota fora do intervalo (0-10).", parent=form); return
            aluno_id = aluno_map.get(aluno_key)
            disc_id = disc_map.get(disc_key)
            try:
                executar_query("INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)", (aluno_id, disc_id, nota))
                messagebox.showinfo("OK", "Nota cadastrada.", parent=form)
                form.destroy()
                carregar()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Erro ao cadastrar nota. Verifique duplicidade.", parent=form)

        ttk.Button(form, text="Salvar", command=salvar).grid(row=3, column=0, pady=10, padx=6)
        ttk.Button(form, text="Cancelar", command=form.destroy).grid(row=3, column=1, pady=10, padx=6, sticky="e")

    def editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione uma nota.", parent=win); return
        item = tree.item(sel[0])["values"]
        nid = item[0]
        # Para edicao, permita apenas a alteracao da nota
        form = tk.Toplevel(win)
        form.title("Editar Nota")
        form.transient(win)
        ttk.Label(form, text=f"ID: {nid}").grid(row=0, column=0, padx=6, pady=6)
        ttk.Label(form, text="Nova Nota (0-10):").grid(row=1, column=0, padx=6, pady=6)
        nota_e = ttk.Entry(form, width=10); nota_e.insert(0, str(item[5])); nota_e.grid(row=1, column=1, padx=6, pady=6)

        def salvar():
            try:
                nova = float(nota_e.get().strip())
            except Exception:
                messagebox.showerror("Erro", "Valor inválido.", parent=form); return
            if nova < 0 or nova > 10:
                messagebox.showerror("Erro", "Fora do intervalo.", parent=form); return
            executar_query("UPDATE notas SET nota = ? WHERE id = ?", (nova, nid))
            messagebox.showinfo("OK", "Nota atualizada.", parent=form)
            form.destroy()
            carregar()

        ttk.Button(form, text="Salvar", command=salvar).grid(row=2, column=0, pady=10, padx=6)
        ttk.Button(form, text="Cancelar", command=form.destroy).grid(row=2, column=1, pady=10, padx=6, sticky="e")

    def excluir():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione uma nota.", parent=win); return
        item = tree.item(sel[0])["values"]
        nid = item[0]
        if messagebox.askyesno("Confirma", f"Confirma exclusão da nota {nid}?", parent=win):
            executar_query("DELETE FROM notas WHERE id = ?", (nid,))
            messagebox.showinfo("OK", "Nota excluída.", parent=win)
            carregar()

    btns = ttk.Frame(win, padding=6)
    btns.pack(fill="x")
    ttk.Button(btns, text="Adicionar", command=adicionar).pack(side="left", padx=4)
    ttk.Button(btns, text="Editar (nota)", command=editar).pack(side="left", padx=4)
    ttk.Button(btns, text="Excluir", command=excluir).pack(side="left", padx=4)
    ttk.Button(btns, text="Fechar", command=win.destroy).pack(side="right", padx=4)

    carregar()

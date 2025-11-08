import tkinter as tk
from tkinter import ttk, messagebox
from funcoes import exportar_dados_csv
from cadastrar_alunos import abrir_tela_alunos
from cadastrar_disciplinas import abrir_tela_disciplinas
from cadastrar_notas import abrir_tela_notas
import sys

root = tk.Tk()
root.title("Sistema de Cadastro Escolar")
root.geometry("480x300")
root.resizable(False, False)

frame = ttk.Frame(root, padding=16)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Sistema de Cadastro Escolar", font=("Segoe UI", 14)).pack(pady=(0, 8))

btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=6)

ttk.Button(btn_frame, text="Cadastro de Alunos", width=28, command=lambda: abrir_tela_alunos(root)).grid(row=0, column=0, padx=6, pady=6)
ttk.Button(btn_frame, text="Cadastro de Disciplinas", width=28, command=lambda: abrir_tela_disciplinas(root)).grid(row=1, column=0, padx=6, pady=6)
ttk.Button(btn_frame, text="Cadastro de Notas", width=28, command=lambda: abrir_tela_notas(root)).grid(row=2, column=0, padx=6, pady=6)

sep = ttk.Separator(frame, orient="horizontal")
sep.pack(fill="x", pady=12)

exp_frame = ttk.Frame(frame)
exp_frame.pack(fill="x", pady=6)
ttk.Label(exp_frame, text="Exportar dados (arquivo):").pack(anchor="w")

def do_csv():
    try:
        paths = exportar_dados_csv()
        messagebox.showinfo("Exportado", f"Arquivos CSV salvos em:\n{paths}", parent=root)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao exportar CSV:\n{e}", parent=root)

btn_e = ttk.Frame(exp_frame)
btn_e.pack(fill="x", pady=6)
ttk.Button(btn_e, text="Exportar CSV", command=do_csv).pack(side="left", padx=6)

if __name__ == "__main__":
    root.mainloop()

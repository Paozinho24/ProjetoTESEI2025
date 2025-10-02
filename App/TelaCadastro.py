# TelaCadastro.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

class TelaCadastro:
    def __init__(self, master, controller, on_saved=None):
        """
        master: janela pai (ex.: self.janela_tela_principal)
        controller: instância do ControllerGeral (já usada no app)
        on_saved: função callback para atualizar a tabela após salvar
        """
        self.controller = controller
        self.on_saved = on_saved
        self.win = tk.Toplevel(master)
        self.win.title("Cadastrar Reagente")
        self.win.transient(master)
        self.win.grab_set()
        self.win.geometry("420x420")

        form = ttk.Frame(self.win, padding=12)
        form.pack(fill="both", expand=True)

        # Campos
        self.ent_nome =self.LinhaForm(form, 0, "Nome*")
        self.ent_formula=self.LinhaForm(form, 1, "Fórmula")
        self.ent_cas=self.LinhaForm(form, 2, "CAS")
        self.cmb_unidade=self.ComboForm(form, 3, "Unidade", ("g", "mg", "kg", "mL", "L", "unid"))
        self.ent_qtd=self.LinhaForm(form, 4, "Quantidade")
        self.ent_armario=self.LinhaForm(form, 5, "Armário")
        self.ent_prateleira=self.LinhaForm(form, 6, "Prateleira")
        self.ent_posicao=self.LinhaForm(form, 7, "Posição")

        # Botões
        btns = ttk.Frame(form)
        btns.grid(row=8, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(btns, text="Salvar", bootstyle="success", command=self.salvar).pack(side="left", padx=6)
        ttk.Button(btns, text="Cancelar", command=self.win.destroy).pack(side="left", padx=6)

        form.grid_columnconfigure(1, weight=1)
        self.ent_nome.focus()

    def LinhaForm(self, parent, row, rotulo):
        ttk.Label(parent, text=rotulo).grid(row=row, column=0, sticky="w", pady=4)
        e = ttk.Entry(parent, width=32)
        e.grid(row=row, column=1, sticky="ew", pady=4)
        return e

    def ComboForm(self, parent, row, rotulo, values):
        ttk.Label(parent, text=rotulo).grid(row=row, column=0, sticky="w", pady=4)
        cb = ttk.Combobox(parent, width=29, values=values, state="normal")
        cb.grid(row=row, column=1, sticky="ew", pady=4)
        return cb

    def salvar(self):
        # Lê e valida
        nome   = self.ent_nome.get().strip()
        if not nome:
            Messagebox.show_warning("Informe o Nome do reagente.", "Atenção")
            self.ent_nome.focus(); return

        formula= self.ent_formula.get().strip()
        cas= self.ent_cas.get().strip() 
        unidade= self.cmb_unidade.get().strip()

        qtd_txt =(self.ent_qtd.get() or "").strip().replace(",", ".")
        quantidade = None
        #Verificação para valores quebrados
        if qtd_txt:
            try:
                quantidade = float(qtd_txt)
            except ValueError:
                Messagebox.show_warning("Quantidade inválida. Use números (ex.: 250 ou 250,5).", "Atenção")
                self.ent_qtd.focus(); 
                return

        armario= self.ent_armario.get().strip()
        prateleira= self.ent_prateleira.get().strip() 
        posicao= self.ent_posicao.get().strip() 

        try:
            # Usa sua função SEM **kwargs (assinatura explícita)
            novo_id = self.controller.cadastrar_Reagente(nome, formula, cas, unidade, quantidade, armario, prateleira, posicao, None )
            Messagebox.ok(f"Reagente cadastrado (Id {novo_id}).", "Sucesso", alert=False)

            # Atualiza tabela na tela principal
            if callable(self.on_saved):
                self.on_saved()

            self.win.destroy()

        except Exception as ex:
            Messagebox.show_error(f"Erro ao cadastrar:\n{ex}", "Erro")

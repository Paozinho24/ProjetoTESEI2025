# TelaCadastro.py
import tkinter as tk
import threading
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
        self.janela = tk.Toplevel(master)
        self.janela.title("Cadastrar Reagente")
        self.janela.transient(master)
        # avoid modal grab that can block other dialogs; keep transient only
        try:
            self.janela.geometry("420x420")
        except Exception:
            pass

        form = ttk.Frame(self.janela, padding=12)
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
        ttk.Button(btns, text="Cancelar", command=self.janela.destroy).pack(side="left", padx=6)

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
            self.ent_nome.focus()
            return

        formula= self.ent_formula.get().strip()
        if not formula:
            Messagebox.show_warning("Informe a Fórmula do reagente.", "Atenção")
            self.ent_formula.focus()
            return
        cas= self.ent_cas.get().strip() 
        if not cas:
            Messagebox.show_warning("Informe o CAS do reagente.", "Atenção")
            self.ent_cas.focus()
            return
        unidade= self.cmb_unidade.get().strip()
        if not unidade:
            Messagebox.show_warning("Informe a Unidade do reagente.", "Atenção")
            try:
                self.cmb_unidade.focus()
            except Exception:
                pass
            return

        qtd_txt =(self.ent_qtd.get() or "").strip().replace(",", ".")
        if not qtd_txt:
            Messagebox.show_warning("Informe a Quantidade do reagente.", "Atenção")
            self.ent_qtd.focus()
            return
        quantidade = None
        # Verificação para valores quebrados
        try:
            quantidade = float(qtd_txt)
        except ValueError:
            Messagebox.show_warning("Quantidade inválida. Use números (ex.: 250 ou 250,5).", "Atenção")
            self.ent_qtd.focus()
            return

        armario= self.ent_armario.get().strip()
        prateleira= self.ent_prateleira.get().strip() 
        posicao= self.ent_posicao.get().strip() 

        # Fecha a janela primeiro para evitar quebra o loop pricipal 
        parent = getattr(self.janela, 'master', None)
        try:
            try:
                #TENTA LIBERAR O GRAP SE ESTIVER PRESENTE
                self.janela.grab_release()
            except Exception:
                pass
            try:
                self.janela.destroy()
            except Exception:
                pass
        except Exception:
            pass

        def PosRodar(novo_id=None, erro=None):
            try:
                if erro is not None:
                    # mostra erro na UI
                    if parent is not None:
                        try:
                            parent.after(0, lambda: Messagebox.show_error(f'Erro ao cadastrar:\n{erro}', 'Erro'))
                        except Exception:
                            Messagebox.show_error(f'Erro ao cadastrar:\n{erro}', 'Erro')
                    else:
                        Messagebox.show_error(f'Erro ao cadastrar:\n{erro}', 'Erro')
                else:
                    if parent is not None:
                        try:
                            parent.after(0, lambda: Messagebox.show_info(f'Reagente cadastrado (Id {novo_id}).', 'Sucesso'))
                        except Exception:
                            Messagebox.show_info(f'Reagente cadastrado (Id {novo_id}).', 'Sucesso')
                    else:
                        Messagebox.show_info(f'Reagente cadastrado (Id {novo_id}).', 'Sucesso')
                if callable(self.on_saved):
                    try:
                        self.on_saved()
                    except Exception as ex:
                        print('Erro ao executar on_saved:', ex)
            except Exception:
                pass

        def Salvar():
            try:
                novo_id = self.controller.cadastrar_Reagente(nome, formula, cas, unidade, quantidade, armario, prateleira, posicao, None )
                if parent is not None:
                    try:
                        parent.after(0, lambda: PosRodar(novo_id, None))
                    except Exception:
                        PosRodar(novo_id, None)
                else:
                    PosRodar(novo_id, None)
            except Exception as ex:
                if parent is not None:
                    try:
                        parent.after(0, lambda: PosRodar(None, ex))
                    except Exception:
                        PosRodar(None, ex)
                else:
                    PosRodar(None, ex)

        threading.Thread(target=Salvar, daemon=True).start()
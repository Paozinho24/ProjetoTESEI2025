# TelaCadastro.py
import tkinter as tk
import threading
import ttkbootstrap as ttk

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
        # avoid modal grab that can block other dialogs; keep transient only
        try:
            self.win.geometry("420x420")
        except Exception:
            pass

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
            print("Aviso: Informe o Nome do reagente.")
            self.ent_nome.focus()
            return

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
                print("Aviso: Quantidade inválida. Use números (ex.: 250 ou 250,5).")
                self.ent_qtd.focus()
                return

        armario= self.ent_armario.get().strip()
        prateleira= self.ent_prateleira.get().strip() 
        posicao= self.ent_posicao.get().strip() 

        # Close this window first to avoid blocking the main loop
        parent = getattr(self.win, 'master', None)
        try:
            try:
                # try releasing grab if present
                self.win.grab_release()
            except Exception:
                pass
            try:
                self.win.destroy()
            except Exception:
                pass
        except Exception:
            pass

        def _after_actions(novo_id=None, erro=None):
            if erro is not None:
                print('Erro ao cadastrar:', erro)
            else:
                print(f'Reagente cadastrado (Id {novo_id}).')
            if callable(self.on_saved):
                try:
                    self.on_saved()
                except Exception as ex:
                    print('Erro ao executar on_saved:', ex)

        def _do_save():
            try:
                novo_id = self.controller.cadastrar_Reagente(nome, formula, cas, unidade, quantidade, armario, prateleira, posicao, None )
                if parent is not None:
                    try:
                        parent.after(0, lambda: _after_actions(novo_id, None))
                    except Exception:
                        _after_actions(novo_id, None)
                else:
                    _after_actions(novo_id, None)
            except Exception as ex:
                if parent is not None:
                    try:
                        parent.after(0, lambda: _after_actions(None, ex))
                    except Exception:
                        _after_actions(None, ex)
                else:
                    _after_actions(None, ex)

        threading.Thread(target=_do_save, daemon=True).start()
import tkinter as tk
import threading
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

class TelaEditarReagente:
    def __init__(self, master, controller, reagente_values: tuple, on_saved=None):
        """
        reagente_values: tuple com os valores da linha selecionada na treeview conforme TelaPrincipal: (Id, Nome, CAS, Formula, Unidade, Quantidade, Armario, Prateleira, Posicao)
        controller: ControllerGeral
        on_saved: callback chamado após salvar para recarregar a tabela
        """
    
        self.controller = controller
        self.on_saved = on_saved
        self.win = tk.Toplevel(master)
        self.win.title("Editar Reagente")
        self.win.transient(master)

        try:
            self.win.geometry("420x420")
        except Exception:
            pass

        form = ttk.Frame(self.win, padding=12)
        form.pack(fill="both", expand=True)

        # Extrai valores com fallback
        id_val = reagente_values[0]
        nome = reagente_values[1] if len(reagente_values) > 1 else ""
        cas = reagente_values[2] if len(reagente_values) > 2 else ""
        formula = reagente_values[3] if len(reagente_values) > 3 else ""
        unidade = reagente_values[4] if len(reagente_values) > 4 else ""
        quantidade = reagente_values[5] if len(reagente_values) > 5 else None
        armario = reagente_values[6] if len(reagente_values) > 6 else ""
        prateleira = reagente_values[7] if len(reagente_values) > 7 else ""
        posicao = reagente_values[8] if len(reagente_values) > 8 else ""

        self.id_val = id_val

        # Campos
        self.ent_nome = self.LinhaForm(form, 0, "Nome*")
        self.ent_formula = self.LinhaForm(form, 1, "Fórmula")
        self.ent_cas = self.LinhaForm(form, 2, "CAS")
        self.cmb_unidade = self.ComboForm(form, 3, "Unidade", ("g", "mg", "kg", "mL", "L", "unid"))
        self.ent_qtd = self.LinhaForm(form, 4, "Quantidade")
        self.ent_armario = self.LinhaForm(form, 5, "Armário")
        self.ent_prateleira = self.LinhaForm(form, 6, "Prateleira")
        self.ent_posicao = self.LinhaForm(form, 7, "Posição")

        # Preenche com valores existentes
        try:
            self.ent_nome.insert(0, nome)
            self.ent_formula.insert(0, formula)
            self.ent_cas.insert(0, cas)
            if unidade:
                self.cmb_unidade.set(unidade)
            if quantidade is not None:
                self.ent_qtd.insert(0, str(quantidade))
            self.ent_armario.insert(0, armario)
            self.ent_prateleira.insert(0, prateleira)
            self.ent_posicao.insert(0, posicao)
        except Exception:
            pass

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

    def confirmar_salvar(self):
        proceed = Messagebox.yesno(
            title="Confirmar edição",
            message=("As alterações neste reagente podem impactar a geração de formulários, "
                    "etiquetas e relatórios que utilizam estes dados.\n\n"
                    "Deseja realmente salvar as alterações?")
        )
        if not proceed:
            return

    def salvar(self):
        self.win.after(100, lambda: self.confirmar_salvar())
        
        nome = self.ent_nome.get().strip()
        if not nome:
            print("Aviso: Informe o Nome do reagente.")
            self.ent_nome.focus()
            return

        formula = self.ent_formula.get().strip()
        cas = self.ent_cas.get().strip()
        unidade = self.cmb_unidade.get().strip()

        qtd_txt = (self.ent_qtd.get() or "").strip().replace(",", ".")
        quantidade = None
        if qtd_txt:
            try:
                quantidade = float(qtd_txt)
            except ValueError:
                print("Aviso: Quantidade inválida. Use números (ex.: 250 ou 250,5).")
                self.ent_qtd.focus()
                return

        armario = self.ent_armario.get().strip()
        prateleira = self.ent_prateleira.get().strip()
        posicao = self.ent_posicao.get().strip()

        parent = getattr(self.win, 'master', None)

        try:
            try:
                self.win.grab_release()
            except Exception:
                pass
            try:
                self.win.destroy()
            except Exception:
                pass
        except Exception:
            pass

        def _after_actions(ok=None, erro=None):
            if erro is not None:
                print('Erro ao atualizar:', erro)
            else:
                print(f'Reagente atualizado (Id {self.id_val}).')
            if callable(self.on_saved):
                try:
                    self.on_saved()
                except Exception as ex:
                    print('Erro ao executar on_saved:', ex)

        def _do_update():
            try:
                self.controller.atualizar_Reagente(self.id_val, nome, formula, cas, unidade, quantidade, armario, prateleira, posicao)
                if parent is not None:
                    try:
                        parent.after(0, lambda: _after_actions(True, None))
                    except Exception:
                        _after_actions(True, None)
                else:
                    _after_actions(True, None)
            except Exception as ex:
                if parent is not None:
                    try:
                        parent.after(0, lambda: _after_actions(None, ex))
                    except Exception:
                        _after_actions(None, ex)
                else:
                    _after_actions(None, ex)

        threading.Thread(target=_do_update, daemon=True).start()
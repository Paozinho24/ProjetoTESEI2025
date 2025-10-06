# TelaCadastro.py
import tkinter as tk
import threading
import ttkbootstrap as ttk
<<<<<<< HEAD
from tkinter import messagebox
=======
from ttkbootstrap.dialogs import Messagebox
from ui_helpers import safe_messagebox
>>>>>>> 1076bdb566cbf2edf22f177a6257595be6c04304

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
<<<<<<< HEAD
        ttk.Button(btns, text="Salvar", bootstyle="success", command=self.tratamento_salvar).pack(side="left", padx=6)
=======
        ttk.Button(btns, text="Salvar", bootstyle="success", command=self.salvar).pack(side="left", padx=6)
>>>>>>> 1076bdb566cbf2edf22f177a6257595be6c04304
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


    def tratamento_salvar(self):
        """
        Valida os campos de Nome, CAS e Quantidade, . 
        Se a validação passar, prossegue para a confirmação.
        """


        # Validar o nome
        nome = self.ent_nome.get().strip()
        if not nome:
<<<<<<< HEAD

            messagebox.showinfo(title='Nome Necessário', message="Insira o nome do reagente")
=======
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", "Informe o Nome do reagente.", "Atenção")
>>>>>>> 1076bdb566cbf2edf22f177a6257595be6c04304
            self.ent_nome.focus()
            return

        formula= self.ent_formula.get().strip()
        if not formula:
<<<<<<< HEAD
            messagebox.showinfo('warning', 'Informe a fórmula do reagente.')
            self.ent_formula.focus()
            return

        #Validar o CAS
        cas = self.ent_cas.get()
        try:
            digitos = cas.replace('-', "").replace(" ", "")
            if not digitos.isdigit() or len(digitos) < 5:
                    raise ValueError('Formato CAS inválido')
            
            checksum_original = int(digitos[-1])
            digitos_verificacao = digitos[:-1]
            soma = 0
            for i, digito_char in enumerate(reversed(digitos_verificacao)):
                multiplicador = i + 1
                soma += int(digito_char) * multiplicador
                
            checksum_calculado = soma % 10

            if checksum_original != checksum_calculado:
                raise ValueError('O CAS inserido não é valido!')
            
        except (ValueError, IndexError):
            messagebox.showerror(title='Cas Inválido', message="O CAS não foi inserido ou está incompleto.")
            self.ent_cas.focus()
            return
        
        #Validar_Unidade
        unidade= self.cmb_unidade.get().strip()
        if not unidade or unidade not in self.cmb_unidade['values']:
            messagebox.showinfo('Warning', 'Informe a unidade do reagente')
=======
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", "Informe a Fórmula do reagente.", "Atenção")
            self.ent_formula.focus()
            return
        cas= self.ent_cas.get().strip() 
        if not cas:
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", "Informe o CAS do reagente.", "Atenção")
            self.ent_cas.focus()
            return
        unidade= self.cmb_unidade.get().strip()
        if not unidade:
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", "Informe a Unidade do reagente.", "Atenção")
>>>>>>> 1076bdb566cbf2edf22f177a6257595be6c04304
            try:
                self.cmb_unidade.focus()
            except Exception:
                pass
            return
<<<<<<< HEAD
        
        quantidade = self.ent_qtd.get().strip()
        qtd_txt =(self.ent_qtd.get() or "").strip().replace(",", ".")
        try:
            quantidade = float(qtd_txt)
            self.salvar(cas, unidade, formula, nome, quantidade)
        except ValueError:
            messagebox.showinfo('Warning', 'Insira uma quantidade inválida. Use números (ex.: 250 ou 250,5)')
=======

        qtd_txt =(self.ent_qtd.get() or "").strip().replace(",", ".")
        if not qtd_txt:
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", "Informe a Quantidade do reagente.", "Atenção")
            self.ent_qtd.focus()
            return
        quantidade = None
        # Verificação para valores quebrados
        try:
            quantidade = float(qtd_txt)
        except ValueError:
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", "Quantidade inválida. Use números (ex.: 250 ou 250,5).", "Atenção")
>>>>>>> 1076bdb566cbf2edf22f177a6257595be6c04304
            self.ent_qtd.focus()
            return


    def salvar(self, cas_org, unidade_org ,formula_org ,nome_org, quantidade_org):

        quantidade=quantidade_org
        cas = cas_org
        unidade = unidade_org
        formula = formula_org
        nome = nome_org
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
<<<<<<< HEAD
                            messagebox.showerror('Erro Cadastro', f'Erro ao Cadastrar: {erro}')

                        except Exception:
                            messagebox.showerror('Erro Cadastro', f'Erro ao Cadastrar: {erro}')
                    else:
                        messagebox.showerror('Erro Cadastro', f'Erro ao cadastrar: {erro}')
=======
                            parent.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao cadastrar:\n{erro}', 'Erro'))
                        except Exception:
                            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao cadastrar:\n{erro}', 'Erro')
                    else:
                        safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao cadastrar:\n{erro}', 'Erro')
>>>>>>> 1076bdb566cbf2edf22f177a6257595be6c04304
                # else:
                #     if parent is not None:
                #         try:
                #             parent.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", f'Reagente cadastrado (Id {novo_id}).', 'Sucesso'))
                #         except Exception:
                #             safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", f'Reagente cadastrado (Id {novo_id}).', 'Sucesso')
                #     else:
                #         safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", f'Reagente cadastrado (Id {novo_id}).', 'Sucesso')
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
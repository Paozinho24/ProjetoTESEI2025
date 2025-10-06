# TelaCadastro.py
import tkinter as tk
import threading
import ttkbootstrap as ttk
from tkinter import messagebox

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
            self.win.geometry("420x420+700+300")
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
        ttk.Button(btns, text="Salvar", bootstyle="success", command=self.tratamento_salvar).pactk(side="left", padx=6)
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
    

    def tratamento_salvar(self):
        """
        Valida os campos de Nome, CAS e Quantidade. 
        Se a validação passar, prossegue para a confirmação.
        """

        nome = self.ent_nome.get().strip()
        cas = self.ent_cas.get().strip().replace("-", "").replace(' ', '')
        qtd_txt = (self.ent_qtd.get() or "").strip().replace(",", ".")

        # 1. Validar o nome
        if not nome:

            messagebox.showinfo(title='Nome Necessário', message="Insira o nome do reagente")
            self.ent_nome.focus()
            return

        # 2. Validar o CAS
        if cas:
            try:
                # O algoritmo de validação de CAS está aqui, mantido por consistência, 
                # embora a regra do CAS seja complexa e possa causar falso negativo.
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
                messagebox.showerror(title='Cas Inválido', message="O CAS inserido não é válido ou está incompleto.")
                self.ent_cas.focus()
                return
        
        # 3. Validar quantidade (se preenchida)
        if qtd_txt:
            try:
                float(qtd_txt)
            except ValueError:
                messagebox.showerror(title='Quantidade Inválida', message='Aviso: Quantidade inválida. Use números (ex.: 250 ou 250,5)')
                self.ent_qtd.focus()
                return
        
        # Se a validação passou, prossegue para a confirmação
        self.confirmar_salvar()

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

        # Fecha a janela primeiro para evitar quebra o loop pricipal 
        parent = getattr(self.win, 'master', None)
        try:
            try:
                #TENTA LIBERAR O GRAP SE ESTIVER PRESENTE
                self.win.grab_release()
            except Exception:
                pass
            try:
                self.win.destroy()
            except Exception:
                pass
        except Exception:
            pass

        def PosRodar(novo_id=None, erro=None):
            if erro is not None:
                print('Erro ao cadastrar:', erro)
            else:
                print(f'Reagente cadastrado (Id {novo_id}).')
            if callable(self.on_saved):
                try:
                    self.on_saved()
                except Exception as ex:
                    print('Erro ao executar on_saved:', ex)


    def confirmar_salvar(self):
        """Exibe o diálogo de confirmação antes de salvar."""
        proceed = messagebox.askyesno(
            title="Confirmar edição",
            message=("As alterações neste reagente podem impactar a geração de formulários, "
                     "etiquetas e relatórios que utilizam estes dados.\n\n"
                     "Deseja realmente salvar as alterações?")
        )
        if proceed:
            # Se confirmado, chama a função final de edição e salvamento assíncrono.
            Salvar()
        else:
            return

        def Salvar(self):
            try:
                novo_id = self.controller.editar_reagentes(nome, formula, cas, unidade, quantidade, armario, prateleira, posicao, None )
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
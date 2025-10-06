import tkinter as tk
import threading 
import ttkbootstrap as ttk
# from ttkbootstrap.dialogs import Messagebox
from tkinter import messagebox

# A classe volta a usar Composição, criando o Toplevel internamente (self.win)
class TelaEditarReagente():
    def __init__(self, master, controller, reagente_values: tuple, on_saved=None):
        """
        reagente_values: tuple com os valores da linha selecionada na treeview (Id, Nome, CAS, Formula, Unidade, Quantidade, Armario, Prateleira, Posicao)
        controller: ControllerGeral
        on_saved: callback chamado após salvar para recarregar a tabela
        """
    
        self.controller = controller
        self.on_saved = on_saved
        # Reintroduzindo self.win (Composição)
        self.win = tk.Toplevel(master) 
        
        self.win.title("Editar Reagente")
        self.win.transient(master)
        # O grab_set foi removido para evitar conflitos com Messagebox.

        try:
            self.win.geometry("420x420+700+300")
        except Exception:
            pass

        # Passa self.win como master para o Frame
        form = ttk.Frame(self.win, padding=12)
        form.pack(fill="both", expand=True)

        # Extrai valores com fallback
        self.id_val = reagente_values[0]
        nome = reagente_values[1] if len(reagente_values) > 1 else ""
        cas = reagente_values[2] if len(reagente_values) > 2 else ""
        formula = reagente_values[3] if len(reagente_values) > 3 else ""
        unidade = reagente_values[4] if len(reagente_values) > 4 else ""
        quantidade = reagente_values[5] if len(reagente_values) > 5 else None
        armario = reagente_values[6] if len(reagente_values) > 6 else ""
        prateleira = reagente_values[7] if len(reagente_values) > 7 else ""
        posicao = reagente_values[8] if len(reagente_values) > 8 else ""

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
                # Garante que a quantidade seja exibida como string
                self.ent_qtd.insert(0, str(quantidade).replace('.', ','))
            self.ent_armario.insert(0, armario)
            self.ent_prateleira.insert(0, prateleira)
            self.ent_posicao.insert(0, posicao)
        except Exception:
            pass

        # Botões
        btns = ttk.Frame(form)
        btns.grid(row=8, column=0, columnspan=2, pady=(12, 0))
        # O botão Salvar chama a função de tratamento/validação
        ttk.Button(btns, text="Salvar", bootstyle="success", command=self.tratamento_salvar).pack(side="left", padx=6)
        # Destruição da janela: self.win.destroy()
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
        """Exibe o diálogo de confirmação antes de salvar."""
        proceed = messagebox.askyesno(
            title="Confirmar edição",
            message=("As alterações neste reagente podem impactar a geração de formulários, "
                     "etiquetas e relatórios que utilizam estes dados.\n\n"
                     "Deseja realmente salvar as alterações?")
        )
        if proceed:
            # Se confirmado, chama a função final de edição e salvamento assíncrono.
            self._finalizar_edicao() 
        else:
            return
        
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

    def _finalizar_edicao(self):
        """
        Extrai os dados finais, fecha a janela de edição e inicia o thread 
        para persistir as alterações via controller.
        """
        # Extrai os dados finais
        nome = self.ent_nome.get().strip()
        formula = self.ent_formula.get().strip()
        cas = self.ent_cas.get().strip()
        unidade = self.cmb_unidade.get().strip()
        
        # Converte para float 
        qtd_txt = (self.ent_qtd.get() or "").strip().replace(",", ".")
        quantidade = float(qtd_txt) if qtd_txt else None
        
        armario = self.ent_armario.get().strip()
        prateleira = self.ent_prateleira.get().strip()
        posicao = self.ent_posicao.get().strip()
        
        # Referencia o widget pai (master) para agendar a thread
        parent = getattr(self.win, 'master', None)

        # 1. Define as ações a serem executadas após o thread de atualização
        def _after_actions(ok=None, erro=None):
            if erro is not None:
                print('Erro ao atualizar:', erro)
                messagebox.showerror('Erro de atualização', f"Erro ao atualizar reagente: \n{erro}")
            else:
                print(f'Reagente atualizado (Id {self.id_val}).')
                messagebox.showinfo("Sucesso", "Reagente atualizado com êxito.")

            if callable(self.on_saved):
                try:
                    # Chama o callback para atualizar a tabela na Tela Principal
                    self.on_saved() 
                except Exception as ex:
                    print('Erro ao executar on_saved:', ex)

        # 2. Define a função a ser executada no thread (chamada ao controller)
        def _do_update():
            try:
                self.controller.atualizar_Reagente(
                    self.id_val, nome, formula, cas, unidade, quantidade, armario, prateleira, posicao
                )
                # Chama a ação final de volta na thread principal do Tkinter
                if parent is not None:
                    parent.after(0, lambda: _after_actions(True, None))
                else:
                    _after_actions(True, None)

            except Exception as ex:
                # Chama a ação final com erro de volta na thread principal do Tkinter
                if parent is not None:
                    parent.after(0, lambda: _after_actions(None, ex))
                else:
                    _after_actions(None, ex)

        # 3. Destruímos a janela Toplevel imediatamente.
        try:
            self.win.destroy() # Destruição via self.win
        except Exception:
            pass

        # 4. Agendamos a INICIALIZAÇÃO da thread de salvamento para o próximo ciclo de eventos
        # da janela principal (parent) com um pequeno delay (1ms). Isso garante que o Tkinter
        # termine de limpar o Messagebox e a janela Toplevel antes de iniciar o trabalho em background.
        if parent:
            parent.after(1, lambda: threading.Thread(target=_do_update, daemon=True).start())
        else:
            # Caso a janela principal não exista (cenário raro), inicia a thread diretamente.
            threading.Thread(target=_do_update, daemon=True).start()

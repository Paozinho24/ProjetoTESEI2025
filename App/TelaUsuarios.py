import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Control import ControllerGeral


class TelaUsuarios:
    def __init__(self, master):
        self.controller = ControllerGeral()
        self.janela = master
        self.janela.title('Gerenciar Usuários')
        self.janela.geometry('700x420')

        container = ttk.Frame(self.janela)
        container.pack(fill='both', expand=True, padx=8, pady=8)

        left = ttk.Frame(container)
        left.pack(side='left', fill='both', expand=True)

        right = ttk.Frame(container)
        right.pack(side='right', fill='y', padx=8)

        # Lista de usuários
        self.tree = ttk.Treeview(left, columns=['Nome', 'CPF', 'Senha', 'Email'], show='headings')
        for c in ['Nome', 'CPF', 'Senha', 'Email']:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(side='left', fill='both', expand=True)

        sb = ttk.Scrollbar(left, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')

        # Formulário
        ttk.Label(right, text='Nome:').pack(anchor='w')
        self.entry_nome = ttk.Entry(right, width=30)
        self.entry_nome.pack()

        ttk.Label(right, text='CPF:').pack(anchor='w', pady=(8,0))
        self.entry_cpf = ttk.Entry(right, width=30)
        self.entry_cpf.pack()

        ttk.Label(right, text='Senha:').pack(anchor='w', pady=(8,0))
        self.entry_senha = ttk.Entry(right, width=30)
        self.entry_senha.pack()

        ttk.Label(right, text='Email:').pack(anchor='w', pady=(8,0))
        self.entry_email = ttk.Entry(right, width=30)
        self.entry_email.pack()

        ttk.Button(right, text='Limpar', bootstyle='secondary', command=self.Limpar).pack(fill='x', pady=(12,4))
        ttk.Button(right, text='Salvar/Editar', bootstyle='success', command=self.Salvar_e_Editar).pack(fill='x', pady=4)
        ttk.Button(right, text='Excluir', bootstyle='danger', command=self.excluir).pack(fill='x', pady=4)

        self.tree.bind('<<TreeviewSelect>>', self.Selecao_Tecnicos)

        self.carregar_lista()

    #Para recarregar a lista quando usar qualquer função
    def carregar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            rows = self.controller.listar_tecnicos()
            for r in rows:
                self.tree.insert('', 'end', values=r)
        except Exception as ex:
            print('Erro ao carregar usuarios:', ex)

    def Selecao_Tecnicos(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])['values']
        # Nome, CPF, Senha, Email
        try:
            self.entry_nome.delete(0, 'end')
            self.entry_nome.insert(0, vals[0])
            # Garantir que o CPF seja mostrado com zeros à esquerda (11 dígitos)
            cpf_val = vals[1]
            try:
                cpf_str = str(cpf_val).zfill(11)
            except Exception:
                cpf_str = str(cpf_val)
            self.entry_cpf.delete(0, 'end')
            self.entry_cpf.insert(0, cpf_str)
            self.entry_senha.delete(0, 'end')
            self.entry_senha.insert(0, vals[2])
            self.entry_email.delete(0, 'end')
            self.entry_email.insert(0, vals[3])
        except Exception:
            pass

    def Limpar(self):
        self.entry_nome.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.entry_email.delete(0, 'end')

    def Salvar_e_Editar(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        senha = self.entry_senha.get()
        email = self.entry_email.get()
        parent = self.janela

        def _after_success():
            try:
                self.carregar_lista()
            except Exception as ex:
                print('Erro ao recarregar lista após salvar:', ex)
            try:
                self.Limpar()
            except Exception as ex:
                print('Erro ao limpar form após salvar:', ex)

        def _do_save():
            try:
                VerificadorDoCpf = self.controller.PegarCPF(cpf)
                if VerificadorDoCpf:
                    self.controller.atualizar_tecnico(nome, cpf, senha, email, cpf)
                else:
                    self.controller.inserir_tecnico(nome, cpf, senha, email)
                # schedule UI updates on main thread
                try:
                    parent.after(0, _after_success)
                except Exception:
                    _after_success()
            except Exception as ex:
                print('Erro ao Salvar_e_Editar usuario:', ex)

        threading.Thread(target=_do_save, daemon=True).start()

    def excluir(self):
        cpf = self.entry_cpf.get()
        if not cpf:
            return
        parent = self.janela

        def _do_delete():
            try:
                self.controller.deletar_tecnico(cpf)
                try:
                    parent.after(0, lambda: (self.carregar_lista(), self.Limpar()))
                except Exception:
                    try:
                        self.carregar_lista()
                    except Exception as ex:
                        print('Erro ao recarregar lista após delete:', ex)
                    try:
                        self.Limpar()
                    except Exception as ex:
                        print('Erro ao limpar form após delete:', ex)
            except Exception as ex:
                print('Erro ao deletar usuario:', ex)

        threading.Thread(target=_do_delete, daemon=True).start()

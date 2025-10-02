<<<<<<< HEAD
import ttkbootstrap as tkk
=======

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
>>>>>>> TesteBackEnd
from TelaPrincipal import TelaPrincipal
from ttkbootstrap.dialogs import Messagebox
from Control import ControllerGeral
from Model import Model

class TelaLogin:
    def __init__(self, master):
        # Estilo e janela
        self.janela = master
        self.janela.title("Login")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)
<<<<<<< HEAD

     
        self.model = Model()
=======
        # expõe a instância para que outras janelas (ex: TelaPrincipal)
        # possam chamar helpers como voltar_para_login()
        try:
            self.janela.tela_instance = self
        except Exception:
            pass
>>>>>>> TesteBackEnd
        self.controller = ControllerGeral()

        # Título
        tkk.Label(self.janela, text="Faça login", font=("TkDefaultFont", 12, "bold")).pack(pady=(20, 10))

        # Usuário (CPF)
        tkk.Label(self.janela, text="Usuário (CPF):").pack(pady=(5, 2))
        self.entry_usuario = tkk.Entry(self.janela, width=30)
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()

        # Senha
        tkk.Label(self.janela, text="Senha:").pack(pady=(10, 2))
        self.entry_senha = tkk.Entry(self.janela, width=30, show="*")
        self.entry_senha.pack(pady=5)

<<<<<<< HEAD
        # Botão Entrar
        tkk.Button(self.janela, text="Entrar", bootstyle="success", command=self._login)\
          .pack(pady=20, ipadx=8, ipady=3)

        # para o botão enter funcionar na tela de login
        self.janela.bind("<Return>", lambda e: self._login())

    #FUNÇÃO DE LOGIN E IGONORE ESSE _ NO COMEÇO TAVA COM SONO 
    def _login(self):
=======
        # Mostrar senha (simples)
        self.var_mostrar = ttk.BooleanVar(value=False)
        ttk.Checkbutton(self.janela, text="Mostrar senha",variable=self.var_mostrar, command=self.MostrarSenha).pack(pady=(2, 6))

        # Lembrar usuário (simples)
        self.var_lembrar = ttk.BooleanVar(value=True)
        ttk.Checkbutton(self.janela, text="Lembrar usuário", variable=self.var_lembrar).pack(pady=(0, 8))

        ttk.Button(self.janela, text="Entrar", bootstyle="success", command=self.login).pack(pady=10, ipadx=8, ipady=3)

        self.janela.bind("<Return>", lambda e: self.login())

    def voltar_para_login(self):
        """Mostra a TelaLogin novamente e limpa a senha."""
        try:
            self.entry_senha.delete(0, 'end')
        except Exception:
            pass
        try:
            self.janela.deiconify()
            self.janela.lift()
        except Exception:
            pass
        try:
            self.entry_usuario.focus_set()
        except Exception:
            pass
        
    def MostrarSenha(self):
        self.entry_senha.configure(show="" if self.var_mostrar.get() else "*")

    def carregarUsuario(self):
        """Carrega o último CPF salvo (se existir) e preenche o campo."""
        try:
            with open(ARQ_USUARIO, "r", encoding="utf-8") as f:
                cpf = f.read().strip()
                if cpf:
                    self.entry_usuario.insert(0, cpf)
        except Exception:
            pass

    def salvarUsuario(self, cpf: str):
        """Salva o último CPF em arquivo texto simples."""
        try:
            with open(ARQ_USUARIO, "w", encoding="utf-8") as f:
                f.write((cpf or "").strip())
        except Exception:
            pass

    def login(self):
        """Valida os campos, autentica no Controller e abre a tela principal."""
>>>>>>> TesteBackEnd
        cpf = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if cpf is None or cpf.strip() == "":
            Messagebox.show_warning("Informe o CPF.", "Atenção")
            self.entry_usuario.focus()
            return

        if senha is None or senha == "":
            Messagebox.show_warning("Informe a senha.", "Atenção")
            self.entry_senha.focus()
            return

        try:
            #VERIFICAÇÃO DO LOGIN COM OS DADOS DO BANCO
            ok = self.controller.login(cpf, senha)
<<<<<<< HEAD
            #ABRE A NOVA TELA SE TUDO FUNCIONAR
            if ok == True:
=======
            if ok:
                if self.var_lembrar.get():
                    self.salvarUsuario(cpf)
                    nome = self.controller.getNomeUsuario(cpf) or "Usuário"
>>>>>>> TesteBackEnd
                Messagebox.ok("Login realizado com sucesso!", "Sucesso", alert=False)
             
                try:
                    self.janela.withdraw()
                except:
                    pass

                self.tela_principal = tkk.Toplevel(self.janela)
                self.tela_principal.title("Tela Principal")
                TelaPrincipal(self.tela_principal, nome_usuario=nome, cpf_usuario=cpf)

                def fechar_tudo():
                    try:
                        self.tela_principal.destroy()
                    except:
                        pass
                    try:
                        self.janela.destroy()
                    except:
                        pass

                self.tela_principal.protocol("WM_DELETE_WINDOW", fechar_tudo)

            else:
                
                Messagebox.show_error("CPF ou senha incorretos.", "Acesso negado")
                
        except Exception as ex:
<<<<<<< HEAD
            
            Messagebox.show_error("Erro ao validar login:\n{}".format(ex), "Erro")
               
             
gui = tkk.Window(themename="flatly")
=======
            Messagebox.show_error(f"Erro ao validar login:\n{ex}", "Erro")


gui = ttk.Window(themename="flatly")
>>>>>>> TesteBackEnd
TelaLogin(gui)
gui.mainloop()

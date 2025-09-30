import ttkbootstrap as tkk
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

     
        self.model = Model()
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

        # Botão Entrar
        tkk.Button(self.janela, text="Entrar", bootstyle="success", command=self._login)\
          .pack(pady=20, ipadx=8, ipady=3)

        # para o botão enter funcionar na tela de login
        self.janela.bind("<Return>", lambda e: self._login())

    #FUNÇÃO DE LOGIN E IGONORE ESSE _ NO COMEÇO TAVA COM SONO 
    def _login(self):
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
            #ABRE A NOVA TELA SE TUDO FUNCIONAR
            if ok == True:
                Messagebox.ok("Login realizado com sucesso!", "Sucesso", alert=False)
             
                try:
                    self.janela.withdraw()
                except:
                    pass

                self.tela_principal = tkk.Toplevel(self.janela)
                self.tela_principal.title("Tela Principal")
                TelaPrincipal(self.tela_principal)

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
            
            Messagebox.show_error("Erro ao validar login:\n{}".format(ex), "Erro")
               
             
gui = tkk.Window(themename="flatly")
TelaLogin(gui)
gui.mainloop()

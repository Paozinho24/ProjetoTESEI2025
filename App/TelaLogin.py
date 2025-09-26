import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from Control import ControllerGeral
from Model import Model

class TelaLogin:
    def __init__(self, master):
        # Estilo e janela
        self.style = tb.Style("flatly")
        self.janela = master
        self.janela.title("Login")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)

     
        self.model = Model()
        self.controller = ControllerGeral()

        # Título
        tb.Label(self.janela, text="Faça login", font=("TkDefaultFont", 12, "bold")).pack(pady=(20, 10))

        # Usuário (CPF)
        tb.Label(self.janela, text="Usuário (CPF):").pack(pady=(5, 2))
        self.entry_usuario = tb.Entry(self.janela, width=30)
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()

        # Senha
        tb.Label(self.janela, text="Senha:").pack(pady=(10, 2))
        self.entry_senha = tb.Entry(self.janela, width=30, show="*")
        self.entry_senha.pack(pady=5)

        # Botão Entrar
        tb.Button(self.janela, text="Entrar", bootstyle="success", command=self._login)\
          .pack(pady=20, ipadx=8, ipady=3)

        # Enter também envia
        self.janela.bind("<Return>", lambda e: self._login())

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
            ok = self.controller.login(cpf, senha)
            if ok:
                Messagebox.ok("Login realizado com sucesso!", "Sucesso", alert=False)
                # aqui você pode abrir a próxima tela se quiser
            else:
                Messagebox.show_error("CPF ou senha incorretos.", "Acesso negado")
        except Exception as ex:
            Messagebox.show_error("Erro ao validar login:\n{}".format(ex), "Erro")

gui = tk.Tk()
TelaLogin(gui)
gui.mainloop()

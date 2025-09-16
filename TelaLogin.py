import tkinter as tk

class TelaLogin:
    def __init__(self, master):
        # Configuração básica
        self.janela = master
        self.janela.title("Login")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)

        # usuário
        self.lbl_usuario = tk.Label(self.janela, text="Usuário:")
        self.lbl_usuario.pack(pady=(40, 5)) 
        self.entry_usuario = tk.Entry(self.janela, width=30)
        self.entry_usuario.pack(pady=5)

        # senha
        self.lbl_senha = tk.Label(self.janela, text="Senha:")
        self.lbl_senha.pack(pady=5)
        #Oculta os caracteres
        self.entry_senha = tk.Entry(self.janela, width=30, show="*") 
        self.entry_senha.pack(pady=5)

        # Botão de envio
        self.btn_login = tk.Button(self.janela, text="Entrar")
        self.btn_login.pack(pady=20)

gui = tk.Tk()
TelaLogin(gui)
gui.mainloop()

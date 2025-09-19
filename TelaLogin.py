import tkinter as tk
import ttkbootstrap as tb 
from ttkbootstrap.dialogs import Messagebox  # <-- acrescentei para feedback visual
import sqlite3
from sqlite3 import Error


class TelaLogin:
    def __init__(self, master):
        # aplica tema (mude para "darkly", "cyborg", "morph" se quiser)
        self.style = tb.Style("flatly")

        # Configuração básica
        self.janela = master
        self.janela.title("Login")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)

        # título simples (opcional)
        self.lbl_titulo = tb.Label(self.janela, text="Faça login", font=("TkDefaultFont", 12, "bold"))
        self.lbl_titulo.pack(pady=(20, 10))

        # usuário (CPF)
        self.lbl_usuario = tb.Label(self.janela, text="Usuário (CPF):")
        self.lbl_usuario.pack(pady=(5, 2))
        self.entry_usuario = tb.Entry(self.janela, width=30)
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()

        # senha
        self.lbl_senha = tb.Label(self.janela, text="Senha:")
        self.lbl_senha.pack(pady=(10, 2))
        # Oculta os caracteres
        self.entry_senha = tb.Entry(self.janela, width=30, show="*")
        self.entry_senha.pack(pady=5)

        # Botão de envio (agora com command)
        self.btn_login = tb.Button(self.janela, text="Entrar", bootstyle="success", command=self._login)
        self.btn_login.pack(pady=20, ipadx=8, ipady=3)

        # Enter também envia
        self.janela.bind("<Return>", lambda e: self._login())

    # ---------- BANCO ----------
    def conexao_banco():
        # dica: prefira caminho absoluto ou string raw r"..."
        caminho = r"ProjetoTESEI2025\BancoDeDados\BancoProjetoTese.db"
        con = None
        try:
            con = sqlite3.connect(caminho)
            print("Conexão estabelecida com sucesso!!!")
            return con
        except Error as ex:
            print(ex)

    # ---------- LÓGICA DE LOGIN ----------
    def _login(self):
        cpf = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()

        if not cpf:
            Messagebox.show_warning("Informe o CPF.", "Atenção")
            self.entry_usuario.focus()
            return
        if not senha:
            Messagebox.show_warning("Informe a senha.", "Atenção")
            self.entry_senha.focus()
            return

        if conexao is None:
            Messagebox.show_error("Sem conexão com o banco de dados.", "Erro")
            return

        try:
            cur = conexao.cursor()
            # Ajuste a tabela/colunas se necessário:
            # Ex.: tabela = 'usuarios', colunas = 'cpf' e 'senha'
            cur.execute("SELECT 1 FROM Tecnicos WHERE CPF = ? AND Senha = ?", (cpf, senha))
            achou = cur.fetchone() is not None

            if achou:
                Messagebox.ok("Login realizado com sucesso!", "Sucesso", alert=False)
                # TODO: abrir a próxima janela/tela do sistema aqui
                # ex.: self._abrir_dashboard()
            else:
                Messagebox.show_error("CPF ou senha incorretos.", "Acesso negado")
        except Error as ex:
            Messagebox.show_error(f"Erro ao consultar o banco:\n{ex}", "Erro")


# cria/usa a conexão (mantendo seu padrão)
conexao = TelaLogin.conexao_banco()

# mantém o padrão do seu código
gui = tk.Tk()
TelaLogin(gui)
gui.mainloop()

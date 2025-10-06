import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from TelaPrincipal import TelaPrincipal
from Control import ControllerGeral

ARQ_USUARIO = "ultimo_usuario.txt"

class TelaLogin:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Login")
        self.janela.geometry("400x320")
        self.janela.resizable(False, False)
        try:
            self.janela.tela_instance = self
        except Exception:
            pass
        self.controller = ControllerGeral()

        ttk.Label(self.janela, text="Faça login", font=("TkDefaultFont", 12, "bold")).pack(pady=(20, 10))

        ttk.Label(self.janela, text="Usuário (CPF):").pack(pady=(5, 2))
        self.entry_usuario = ttk.Entry(self.janela, width=30)
        self.entry_usuario.pack(pady=5)
        self.carregarUsuario()  # preenche se existir
        self.entry_usuario.focus()

        ttk.Label(self.janela, text="Senha:").pack(pady=(10, 2))
        self.entry_senha = ttk.Entry(self.janela, width=30, show="*")
        self.entry_senha.pack(pady=5)

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
        cpf = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not cpf.strip():
            Messagebox.show_warning("Informe o CPF.", "Atenção")
            self.entry_usuario.focus()
            return
        if not senha:
            Messagebox.show_warning("Informe a senha.", "Atenção")
            self.entry_senha.focus()
            return

        try:
            ok = self.controller.login(cpf, senha)
            if ok:
                if self.var_lembrar.get():
                    self.salvarUsuario(cpf)
                    nome = self.controller.getNomeUsuario(cpf) or "Usuário"
                # Messagebox.ok("Login realizado com sucesso!", "Sucesso", alert=False)

                try:
                    self.janela.withdraw()
                except Exception:
                    pass

                self.tela_principal = ttk.Toplevel(self.janela)
                self.tela_principal.title("Tela Principal")
                TelaPrincipal(self.tela_principal, nome_usuario=nome, cpf_usuario=cpf)

                def fechar_tudo():
                    try:
                        self.tela_principal.destroy()
                    except Exception:
                        pass
                    try:
                        self.janela.destroy()
                    except Exception:
                        pass

                self.tela_principal.protocol("WM_DELETE_WINDOW", fechar_tudo)
            else:
                Messagebox.show_error("CPF ou senha incorretos.", "Acesso negado")
        except Exception as ex:
            Messagebox.show_error(f"Erro ao validar login:\n{ex}", "Erro")


gui = ttk.Window(themename="flatly")
TelaLogin(gui)
gui.mainloop()
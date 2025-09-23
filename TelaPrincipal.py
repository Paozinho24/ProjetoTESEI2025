import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class TelaPrincipal():
    def __init__(self, master):
        self.janela_tela_principal=master

        ##!!!!!!!!!!!!ESSA FUNÇÃO PODE DAR ERRO NO LINUX!!!!!!!!
        self.janela_tela_principal.state('zoomed')

        #Alterando o Style dos botões:
        style=ttk.Style()
        style.configure('TButton', font=('TkDefaultFont', 12, 'bold'), padding=10)
        style.configure('primary.TButton', font=('TkDefaultFont', 13, 'bold'), padding=10)


        # self.janela_tela_principal.resizable(0,0)
        self.janela_tela_principal.title('Tela Principal')

        #Declarando os Frames (Containers):
        self.frame_superior = ttk.Frame(self.janela_tela_principal, bootstyle='primary', height=130)
        self.frame_logout = ttk.Frame(self.frame_superior, bootstyle='primary', height=130, width=200)
        self.frame_inferior_botoes = ttk.Frame(self.janela_tela_principal, height=500, width=800)

            #Declarando os Frames Estéticos:
        self.frame_azul_acima =ttk.Frame(self.janela_tela_principal, bootstyle='info', height=40)
        self.frame_azul_direita =ttk.Frame(self.janela_tela_principal, bootstyle='info', width=20)
        self.frame_azul_esquerda =ttk.Frame(self.janela_tela_principal, bootstyle='info', width=20)
        self.frame_azul_abaixo =ttk.Frame(self.janela_tela_principal, bootstyle='info', height=20)

        #Ajustando o Treeview (tabela):
        self.tabela = ttk.Treeview(self.janela_tela_principal, columns=['ID', 'Nome', 'CAS', 'Fórmula', 'Unidade', 'Quantidade', 'Armário', 'Prateleira', 'Posição'], height=30, show='headings', bootstyle='dark')

            #Inserindo as colunas na TreeView com seus respectivos tamanhos:
        for coluna in self.tabela['columns']:
            self.tabela.column(f'{coluna}', minwidth=0, width=170)

            #Declarando os titulos que serão mostrados nas colunas da tabela:
        for titulo in self.tabela['columns']:
            self.tabela.heading(f'{titulo}', text=f'{titulo}')

            #Declarando e inserindo a Scrollbar na tabela:
        self.scrollbar_tabela = ttk.Scrollbar(self.janela_tela_principal, orient='vertical', command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=self.scrollbar_tabela.set)

        #Declarando as Labels:
        self.lbl_logout=ttk.Label(self.frame_logout,text=f'Olá, -NomeUsuario-', bootstyle='inverse-primary', font=('TkDefaultFont', 12, 'bold'))

        #Declarando os botões:
        self.botao_logout=ttk.Button(self.frame_logout,text='Logout',bootstyle='secondary')
        self.botao_cadastrar=ttk.Button(self.frame_inferior_botoes, text='Cadastrar', bootstyle='primary', width=15)
        self.botao_retirar=ttk.Button(self.frame_inferior_botoes, text='Retirar', bootstyle='primary', width=15)
        self.botao_relatorios=ttk.Button(self.frame_inferior_botoes, text='Relatórios', bootstyle='primary', width=15)


        #Gerenciando pelo Pack:

            #Gerenciando o frame superior:
        self.frame_superior.pack(side='top', fill='x')
        self.frame_superior.pack_propagate(False)
        self.frame_logout.pack(side='right', padx=40)
        self.frame_logout.pack_propagate(False)
        self.botao_logout.pack(side='bottom', pady=10)
        self.lbl_logout.pack(side='bottom', pady=10)
            #Gerenciando estética:
        self.frame_azul_abaixo.pack(side='bottom', fill='x')
        self.frame_azul_acima.pack(side='top', fill='x')
        self.frame_azul_direita.pack(side='right', fill='y')
        self.frame_azul_esquerda.pack(side='left', fill='y')
        self.tabela.pack(side='top', pady=30)

            #Gerenciando o frame inferior:
        self.frame_inferior_botoes.pack(side='bottom')
        self.frame_inferior_botoes.pack_propagate(False)
        self.botao_cadastrar.pack(side='left')
        self.botao_retirar.pack(side='right')
        self.botao_relatorios.pack(expand=True)


gui=ttk.Window(themename='flatly')
TelaPrincipal(gui)
gui.mainloop()
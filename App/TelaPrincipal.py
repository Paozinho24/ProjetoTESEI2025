import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Control import ControllerGeral
from Model import Model

class TelaPrincipal():
    def __init__(self, master):
        self.model = Model()
        self.controller = ControllerGeral()
        self.janela_tela_principal = master

        # Pode falhar no Linux; 
        self.janela_tela_principal.state('zoomed')

        style = ttk.Style()
        style.configure('TButton', font=('TkDefaultFont', 12, 'bold'), padding=10)
        style.configure('primary.TButton', font=('TkDefaultFont', 13, 'bold'), padding=10)

        self.janela_tela_principal.title('Tela Principal')

        # Frames
        self.frame_superior = ttk.Frame(self.janela_tela_principal, bootstyle='primary', height=130)
        self.frame_logout = ttk.Frame(self.frame_superior, bootstyle='primary', height=130, width=200)
        self.frame_inferior_botoes = ttk.Frame(self.janela_tela_principal, height=500, width=800)

        # EstéticosFRESCOS
        self.frame_azul_acima = ttk.Frame(self.janela_tela_principal, bootstyle='info', height=40)
        self.frame_azul_direita = ttk.Frame(self.janela_tela_principal, bootstyle='info', width=20)
        self.frame_azul_esquerda = ttk.Frame(self.janela_tela_principal, bootstyle='info', width=20)
        self.frame_azul_abaixo = ttk.Frame(self.janela_tela_principal, bootstyle='info', height=20)

        # TABELA BRABA
        self.tabela = ttk.Treeview(
            self.janela_tela_principal,
            columns=['ID', 'Nome', 'CAS', 'Fórmula', 'Unidade', 'Quantidade', 'Armário', 'Prateleira', 'Posição'],
            height=30,
            show='headings',
            bootstyle='dark'
        )

        for coluna in self.tabela['columns']:
            self.tabela.column(coluna, minwidth=0, width=170)

        for titulo in self.tabela['columns']:
            self.tabela.heading(titulo, text=titulo)

        #scrolbbar bolada demais
        self.scrollbar_tabela = ttk.Scrollbar(self.janela_tela_principal, orient='vertical', command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=self.scrollbar_tabela.set)

        # Labels e botões
        self.lbl_logout = ttk.Label(self.frame_logout, text='Olá, -NomeUsuario-', bootstyle='inverse-primary', font=('TkDefaultFont', 12, 'bold'))

        self.botao_logout = ttk.Button(self.frame_logout, text='Logout', bootstyle='secondary')
        self.botao_cadastrar = ttk.Button(self.frame_inferior_botoes, text='Cadastrar', bootstyle='primary', width=15)
        self.botao_retirar = ttk.Button(self.frame_inferior_botoes, text='Retirar', bootstyle='primary', width=15)
        self.botao_relatorios = ttk.Button(self.frame_inferior_botoes, text='Relatórios', bootstyle='primary', width=15)

        # Packs
        self.frame_superior.pack(side='top', fill='x')
        self.frame_superior.pack_propagate(False)
        self.frame_logout.pack(side='right', padx=40)
        self.frame_logout.pack_propagate(False)
        self.botao_logout.pack(side='bottom', pady=10)
        self.lbl_logout.pack(side='bottom', pady=10)

        self.frame_azul_abaixo.pack(side='bottom', fill='x')
        self.frame_azul_acima.pack(side='top', fill='x')
        self.frame_azul_direita.pack(side='right', fill='y')
        self.frame_azul_esquerda.pack(side='left', fill='y')

        # Tabela + Scrollbar
        self.tabela.pack(side='top', pady=30)
        self.scrollbar_tabela.pack(side='right', fill='y')   # <-- garantir que aparece

        self.frame_inferior_botoes.pack(side='bottom')
        self.frame_inferior_botoes.pack_propagate(False)
        self.botao_cadastrar.pack(side='left')
        self.botao_retirar.pack(side='right')
        self.botao_relatorios.pack(expand=True)

        # === CARREGAR DADOS NA TABELA ===
        self.carregar_dados_tabela()   # sem filtro; se quiser, passe um nome parcial que vai buscar diretamente um reagente pelo nome , vamos incrementar no futuro

    def carregar_dados_tabela(self, nome_parcial=None):

        try:
            # Buscar dados via controller usando o nome_parcial
            linhas = self.controller.listar_reagentes_localizacao(nome_parcial)
            print(linhas)
            # 3) Inserir no Treeview
            # Ordem precisa bater com self.tabela['columns']
            for linha in linhas:
                # linha vem como tupla:
                # (Id, Nome, CAS, Formula, Unidade, Quantidade, Armario, Prateleira, Posicao)
                self.tabela.insert('', 'end', values=(
                    linha[0],  # ID
                    linha[1],  # Nome
                    linha[2],  # CAS
                    linha[3],  # Fórmula
                    linha[4],  # Unidade
                    linha[5],  # Quantidade
                    linha[6],  # Armário
                    linha[7],  # Prateleira
                    linha[8],  # Posição
                ))
        except Exception as ex:
            # Se quiser, exiba com Messagebox; aqui mantenho simples:
            print("Erro ao carregar dados da tabela:", ex)




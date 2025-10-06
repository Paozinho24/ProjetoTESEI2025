
from importlib import import_module
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from Control import ControllerGeral
from Model import Model
from TelaCadastro import TelaCadastro
from TelaEditarReagente import TelaEditarReagente
from ui_helpers import safe_messagebox


class TelaPrincipal():
    def __init__(self, master, nome_usuario="Usuário", cpf_usuario=None):
        self.model = Model()
        self.controller = ControllerGeral()
        # PARENT VISÍVEL E CONSISTENTE
        self.janela_tela_principal = master

        # Pode falhar no Linux; não é crítico
        try:
            self.janela_tela_principal.state('zoomed')
        except Exception:
            pass

        style = ttk.Style()
        style.configure('TButton', font=('TkDefaultFont', 12, 'bold'), padding=10)
        style.configure('primary.TButton', font=('TkDefaultFont', 13, 'bold'), padding=10)

        self.janela_tela_principal.title('Tela Principal')

        # --- MOLDURAS (bordas estéticas) ---
        self.frame_azul_acima    = ttk.Frame(self.janela_tela_principal, bootstyle='info', height=40)
        self.frame_azul_abaixo   = ttk.Frame(self.janela_tela_principal, bootstyle='info', height=20)
        self.frame_azul_esquerda = ttk.Frame(self.janela_tela_principal, bootstyle='info', width=20)
        self.frame_azul_direita  = ttk.Frame(self.janela_tela_principal, bootstyle='info', width=20)

        # Pack das bordas PRIMEIRO
        self.frame_azul_acima.pack(side='top', fill='x')
        self.frame_azul_abaixo.pack(side='bottom', fill='x')
        self.frame_azul_esquerda.pack(side='left', fill='y')
        self.frame_azul_direita.pack(side='right', fill='y')

        # CONTAINER CENTRAL que vai crescer e conter todo o conteúdo 
        container = ttk.Frame(self.janela_tela_principal)
        container.pack(side='top', fill='both', expand=True)

        # TOPO (barra superior) 
        self.frame_superior = ttk.Frame(container, bootstyle='primary')
        self.frame_superior.pack(side='top', fill='x')

        # Área logout dentro do topo
        self.frame_logout = ttk.Frame(self.frame_superior, bootstyle='primary')
        self.frame_logout.pack(side='right', padx=40, pady=10)
        self.lbl_logout = ttk.Label(self.frame_logout,text=f'Olá, {nome_usuario}',bootstyle='inverse-primary',font=('TkDefaultFont', 12, 'bold'))
        self.lbl_logout.pack(side='left', padx=(0,10))
        self.botao_logout = ttk.Button(self.frame_logout, text='Logout', bootstyle='secondary', command=self.logout)
        self.botao_logout.pack(side='left')
        # Se for admin (CPF padrão 00000000000), adiciona botão de gerenciamento de usuários
        try:
            if cpf_usuario == 'admin':
                self.botao_admin = ttk.Button(self.frame_logout, text='Usuários', bootstyle='warning', command=self.abrirTelaUsuarios)
                self.botao_admin.pack(side='left', padx=(8,0))
        except Exception:
            pass

        # MEIO (onde fica a TABELA) 
        area_meio = ttk.Frame(container)
        area_meio.pack(side='top', fill='both', expand=True, padx=8, pady=8)

        # TABELA
        self.tabela = ttk.Treeview(
            area_meio,
            columns=['ID', 'Nome', 'CAS', 'Fórmula', 'Unidade', 'Quantidade', 'Armário', 'Prateleira', 'Posição'],
            show='headings',
            bootstyle='dark'
        )

        # Cabeçalhos e colunas
        for titulo in self.tabela['columns']:
            self.tabela.heading(titulo, text=titulo)
            
        self.tabela.column('ID', width=80, anchor='center', stretch=False)
        self.tabela.column('Nome', width=220)
        self.tabela.column('CAS', width=120, anchor='center')
        self.tabela.column('Fórmula', width=120, anchor='center')
        self.tabela.column('Unidade', width=100, anchor='center')
        self.tabela.column('Quantidade', width=120, anchor='center')
        self.tabela.column('Armário', width=120, anchor='center')
        self.tabela.column('Prateleira', width=120, anchor='center')
        self.tabela.column('Posição', width=100, anchor='center')

        # Scrollbar vertical (AGORA com pack)
        self.scrollbar_tabela = ttk.Scrollbar(area_meio, orient='vertical', command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=self.scrollbar_tabela.set)

        # Layout do miolo
        self.tabela.pack(side='left', fill='both', expand=True)
        self.scrollbar_tabela.pack(side='right', fill='y')

        # --- RODAPÉ (botões inferiores) ---
        self.frame_inferior_botoes = ttk.Frame(container)
        self.frame_inferior_botoes.pack(side='bottom', fill='x', pady=(4, 8))

        self.botao_cadastrar  = ttk.Button(self.frame_inferior_botoes,text='Cadastrar', bootstyle='primary', width=15, command=self.abrirCadastro)
        self.botao_relatorios = ttk.Button(self.frame_inferior_botoes, text='Relatórios', bootstyle='primary', width=15, command=self.abrirRelatorios)
        self.botao_editar = ttk.Button(self.frame_inferior_botoes, text='Editar', bootstyle='warning' , width=15 , padding=(10), command=self.abrirEditar)
        self.botao_retirar    = ttk.Button(self.frame_inferior_botoes, text='Retirar',     bootstyle='primary', width=15, command=self.abrirRetirar)

        self.botao_cadastrar.pack(side='left', padx=8)
        self.botao_relatorios.pack(side='left', padx=8)
        self.botao_editar.pack(side="left", padx=8)
        self.botao_retirar.pack(side='right', padx=8)

        # === CARREGAR DADOS NA TABELA ===
        self.carregar_dados_tabela()
        
        
    # #Funções de da Tela
    def logout(self):
        # Tenta recuperar a janela pai (se existir)
        TelaPai = self.janela_tela_principal.master if hasattr(self.janela_tela_principal, 'master') else None

        # Destrói a janela principal atual
        try:
            self.janela_tela_principal.destroy()
        except Exception:
            pass

        # Se houver janela pai, tenta reexibi-la e limpar a senha
        if TelaPai:
            try:
                TelaPai.deiconify()
                TelaPai.lift()
            except Exception:
                pass

            # Se a instância do login estiver exposta, chame o helper
            if hasattr(TelaPai, 'tela_instance'):
                tela_inst = TelaPai.tela_instance
                if hasattr(tela_inst, 'voltar_para_login'):
                    try:
                        tela_inst.voltar_para_login()
                    except Exception:
                        pass
            
    def abrirCadastro(self):
        # Abre a tela e, ao salvar, chama recarregarTabela
        TelaCadastro(self.janela_tela_principal, self.controller, on_saved=self.recarregarTabela)

    def abrirTelaUsuarios(self):
        try:
            topo = ttk.Toplevel(self.janela_tela_principal)
            from TelaUsuarios import TelaUsuarios
            TelaUsuarios(topo)
        except Exception as ex:
            print('Erro ao abrir TelaUsuarios:', ex)

    def _parent(self):
        # SEMPRE use a janela principal visível como parent
        return self.janela_tela_principal

    def abrirEditar(self):
        # Abre a tela de edição para o reagente selecionado na treeview
        sel = self.tabela.selection()
        if not sel:
            # Sempre usa o parent correto e título claro
            self.janela_tela_principal.after(0, lambda: safe_messagebox(self._parent(), "warning", "Selecione um reagente para editar.", "Aviso"))
            return
        try:
            item = self.tabela.item(sel[0])
            vals = item.get('values', ())
            # Abre a tela de edição em top-level
            TelaEditarReagente(self.janela_tela_principal, self.controller, vals, on_saved=self.recarregarTabela)
        except Exception as ex:
            self.janela_tela_principal.after(0, lambda: safe_messagebox(self._parent(), "warning", "Erro ao abrir a tela de edição: " + str(ex), "Aviso"))

    def abrirRelatorios(self):
        try:
            from TelaRelatorios import TelaRelatorios
            TelaRelatorios(self.janela_tela_principal, self.controller)
        except Exception as ex:
            self.janela_tela_principal.after(0, lambda: safe_messagebox(self._parent(), "warning", "Erro ao abrir TelaRelatorios: " + str(ex), "Aviso"))

    def abrirRetirar(self):
        sel = self.tabela.selection()
        if not sel:
            self.janela_tela_principal.after(0, lambda: safe_messagebox(self._parent(), "warning", "Selecione um reagente para retirar.", "Aviso"))
            return
        try:
            item = self.tabela.item(sel[0])
            vals = item.get('values', ())
            from TelaRetirar import TelaRetirar
            TelaRetirar(self.janela_tela_principal, self.controller, vals, on_done=self.recarregarTabela)
        except Exception as ex:
            self.janela_tela_principal.after(0, lambda: safe_messagebox(self._parent(), "warning", "Erro ao abrir a tela de retirada: " + str(ex), "Aviso"))

    def recarregarTabela(self):
        # Limpa e recarrega a Treeview
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        self.carregar_dados_tabela()

    # Carrega os dados da Tabela
    def carregar_dados_tabela(self):
        try:
            linhas = self.controller.listar_reagentes_localizacao()
            for linha in linhas:
                self.tabela.insert('', 'end', values=(
                    linha[0], linha[1], linha[2], linha[3], linha[4],
                    linha[5], linha[6], linha[7], linha[8]
                ))
        except Exception as ex:
            self.janela_tela_principal.after(0, lambda: safe_messagebox(self._parent(), "warning", "Erro ao carregar dados da tabela: " + str(ex), "Aviso"))

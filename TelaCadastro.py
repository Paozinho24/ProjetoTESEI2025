import ttkbootstrap as ttk
from ttkbootstrap.constants import *


#Utilizada para instanciá-la dentro da Tela Principal (facilitar a utilização do toplevel da tela cadastro)
class TelaCadastro(ttk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastrar Reagente")
        self.geometry("900x700+700+150")
        self.resizable(True, True)

        # estilo das labels
        style = ttk.Style()
        style.configure('primary.TLabel', font=('TkDefaultFont', 14), padding=5)

        # containers principais
        cnt_superior = ttk.Frame(self, bootstyle='primary', height=100)
        cnt_form = ttk.Frame(self, padding=16)

        # containers dos campos
        cnt_nome = ttk.Frame(cnt_form)
        cnt_formula = ttk.Frame(cnt_form)
        cnt_cas = ttk.Frame(cnt_form)
        cnt_unidade = ttk.Frame(cnt_form)
        cnt_quantidade = ttk.Frame(cnt_form)
        cnt_prateleira = ttk.Frame(cnt_form)
        cnt_armario = ttk.Frame(cnt_form)
        cnt_posicao = ttk.Frame(cnt_form)

        # label do cabeçalho
        lbl_cadastro = ttk.Label(
            cnt_superior, text='Cadastro',
            bootstyle='inverse-primary', font=('TkDefaultFont', 16, 'bold'), padding=12
        )

        # labels de cada campo
        lbl_nome = ttk.Label(cnt_nome, text='Nome:', style='primary.TLabel', anchor="w")
        lbl_formula = ttk.Label(cnt_formula, text='Fórmula:', style='primary.TLabel', anchor="w")
        lbl_cas = ttk.Label(cnt_cas, text='CAS:', style='primary.TLabel', anchor="w")
        lbl_unidade = ttk.Label(cnt_unidade, text='Unidade:', style='primary.TLabel', anchor="w")
        lbl_quantidade = ttk.Label(cnt_quantidade, text='Quantidade:', style='primary.TLabel', anchor="w")
        lbl_prateleira = ttk.Label(cnt_prateleira, text='Prateleira:', style='primary.TLabel', anchor="w")
        lbl_armario = ttk.Label(cnt_armario, text='Armário:', style='primary.TLabel', anchor="w")
        lbl_posicao = ttk.Label(cnt_posicao, text='Posição:', style='primary.TLabel', anchor="w")

        # entradas de texto
        ent_nome = ttk.Entry(cnt_nome)
        ent_formula = ttk.Entry(cnt_formula)
        ent_cas = ttk.Entry(cnt_cas)
        ent_armario = ttk.Entry(cnt_armario)

        # listas para as combobox
        values_qtd = [i for i in range(1, 51)]
        values_prateleira = [i for i in range(1, 21)]
        values_posicao = [i for i in range(1, 11)]
        values_armario = [i for i in range(1, 31)]

        # combobox
        cbb_quantidade = ttk.Combobox(cnt_quantidade, values=values_qtd, state='readonly')
        cbb_prateleira = ttk.Combobox(cnt_prateleira, values=values_prateleira, state='readonly')
        cbb_posicao = ttk.Combobox(cnt_posicao, values=values_posicao, state='readonly')
        cbb_unidade = ttk.Combobox(cnt_unidade, values=['Litros', 'Mililitros', 'Quilos', 'Gramas'], state='readonly')
        cbb_armario = ttk.Combobox(cnt_armario, values=values_armario, state='readonly')

        # valores iniciais
        cbb_unidade.set('Litros')
        cbb_quantidade.set(1)
        cbb_prateleira.set(1)
        cbb_posicao.set(1)

        # ação do botão
        def on_cadastrar():
            dados = [
                ent_nome.get().strip(),
                ent_formula.get().strip(),
                ent_cas.get().strip(),
                cbb_unidade.get().strip(),
                int(cbb_quantidade.get()) if cbb_quantidade.get() else None,
                str(cbb_armario.get()) if cbb_armario.get() else None,
                int(cbb_prateleira.get()) if cbb_prateleira.get() else None,
                int(cbb_posicao.get()) if cbb_posicao.get() else None,
            ]
            print(dados)

        # botão
        btn_cadastrar = ttk.Button(self, text='Cadastrar', command=on_cadastrar, bootstyle="primary")
        # estilo do botão cadastrar
        style.configure(
            'Cadastrar.TButton',
            font=('TkDefaultFont', 14, 'bold'),   # aumenta o tamanho da fonte
            padding=15                            # aumenta o espaço interno
        )

        # cabeçalho
        cnt_superior.grid(row=0, column=0, sticky='ew')
        cnt_superior.grid_columnconfigure(0, weight=1)
        lbl_cadastro.grid(row=0, column=0, sticky='w', padx=16, pady=(6,6))

        # container do formulário
        cnt_form.grid(row=1, column=0, sticky='nsew', padx=24, pady=20)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        cnt_form.grid_columnconfigure(0, weight=1, uniform="cols")
        cnt_form.grid_columnconfigure(1, weight=1, uniform="cols")

        # organização dos grupos em 2 colunas
        cnt_nome.grid(row=0, column=0, sticky="nsew", padx=(0,12), pady=(0,12))
        cnt_formula.grid(row=0, column=1, sticky="nsew", padx=(12,0), pady=(0,12))

        cnt_cas.grid(row=1, column=0, sticky="nsew", padx=(0,12), pady=12)
        cnt_unidade.grid(row=1, column=1, sticky="nsew", padx=(12,0), pady=12)

        cnt_quantidade.grid(row=2, column=0, sticky="nsew", padx=(0,12), pady=12)
        cnt_prateleira.grid(row=2, column=1, sticky="nsew", padx=(12,0), pady=12)

        cnt_armario.grid(row=3, column=0, sticky="nsew", padx=(0,12), pady=12)
        cnt_posicao.grid(row=3, column=1, sticky="nsew", padx=(12,0), pady=12)

        # labels e campos dentro dos grupos
        for grp in (cnt_nome, cnt_formula, cnt_cas, cnt_unidade, cnt_quantidade, cnt_prateleira, cnt_armario, cnt_posicao):
            grp.grid_columnconfigure(0, weight=1)

        lbl_nome.grid(row=0, column=0, sticky="w", pady=(0,4)); ent_nome.grid(row=1, column=0, sticky="ew")
        lbl_formula.grid(row=0, column=0, sticky="w", pady=(0,4)); ent_formula.grid(row=1, column=0, sticky="ew")
        lbl_cas.grid(row=0, column=0, sticky="w", pady=(0,4)); ent_cas.grid(row=1, column=0, sticky="ew")
        lbl_unidade.grid(row=0, column=0, sticky="w", pady=(0,4)); cbb_unidade.grid(row=1, column=0, sticky="ew")
        lbl_quantidade.grid(row=0, column=0, sticky="w", pady=(0,4)); cbb_quantidade.grid(row=1, column=0, sticky="ew")
        lbl_prateleira.grid(row=0, column=0, sticky="w", pady=(0,4)); cbb_prateleira.grid(row=1, column=0, sticky="ew")
        lbl_armario.grid(row=0, column=0, sticky="w", pady=(0,4)); ent_armario.grid(row=1, column=0, sticky="ew")
        lbl_posicao.grid(row=0, column=0, sticky="w", pady=(0,4)); cbb_posicao.grid(row=1, column=0, sticky="ew")

        # botão cadastrar
        btn_cadastrar.grid(row=2, column=0, pady=(4,24))

        # foco inicial e enter
        ent_nome.focus_set()
        self.bind("<Return>", lambda e: on_cadastrar())

if __name__ == "__main__":
    gui = ttk.Window(themename='flatly')
    TelaCadastro(gui)
    gui.mainloop()

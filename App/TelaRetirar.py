import ttkbootstrap as ttk
import threading
from ttkbootstrap.dialogs import Messagebox
from ui_helpers import safe_messagebox

class TelaRetirar:
    def __init__(self, master, controller: object, reagente_vals: tuple, on_done: callable = None):
        """REAGENTES FORMA: tuple retornada pela Treeview (Id, Nome, CAS, Formula, Unidade, Quantidade, Armario, Prateleira, Posicao)
        on_done: callback executado após retirada para recarregar tabelas
        """
        self.controller = controller
        self.on_done = on_done
        self.reagente_vals = reagente_vals

        self.janela = ttk.Toplevel(master)
        self.janela.title('Retirar Reagente')
        self.janela.transient(master)
        # Não usar grab_set aqui: bloqueia diálogos (Messagebox/filedialogs) em algumas plataformas

        body = ttk.Frame(self.janela, padding=12)
        body.pack(fill='both', expand=True)

        ttk.Label(body, text=f"+Reagente: {reagente_vals[1]}").grid(row=0, column=0, columnspan=2, sticky='w')
        # Exibe quantidade atual e unidade (se disponível)
        unidade = ''
        try:
            unidade = reagente_vals[4] or ''
        except Exception:
            unidade = ''
        ttk.Label(body, text=f"+Quantidade atual: {reagente_vals[5]} {unidade}").grid(row=1, column=0, columnspan=2, sticky='w')

        ttk.Label(body, text='Quantidade a retirar:').grid(row=2, column=0, sticky='w', pady=(8,0))
        self.entry_qtd = ttk.Entry(body, width=20)
        self.entry_qtd.grid(row=2, column=1, sticky='ew', pady=(8,0))

        ttk.Label(body, text='Motivo:').grid(row=3, column=0, sticky='w', pady=(8,0))
        self.entry_motivo = ttk.Entry(body, width=40)
        self.entry_motivo.grid(row=3, column=1, sticky='ew', pady=(8,0))

        ttk.Label(body, text='Responsável:').grid(row=4, column=0, sticky='w', pady=(8,0))
        self.entry_resp = ttk.Entry(body, width=40)
        self.entry_resp.grid(row=4, column=1, sticky='ew', pady=(8,0))

        ttk.Label(body, text='Projeto:').grid(row=5, column=0, sticky='w', pady=(8,0))
        self.entry_projeto = ttk.Entry(body, width=40)
        self.entry_projeto.grid(row=5, column=1, sticky='ew', pady=(8,0))

        btns = ttk.Frame(body)
        btns.grid(row=6, column=0, columnspan=2, pady=(12,0))

        ttk.Button(btns, text='Confirmar', bootstyle='success', command=self.confirmar).pack(side='left', padx=6)
        ttk.Button(btns, text='Cancelar', command=self.janela.destroy).pack(side='left', padx=6)

        body.grid_columnconfigure(1, weight=1)

    def confirmar(self):
        qtd = self.entry_qtd.get().strip()
        motivo = self.entry_motivo.get().strip()
        resp = self.entry_resp.get().strip()
        try:
            projeto = self.entry_projeto.get().strip()
            # executa em thread para não bloquear UI
            threading.Thread(target=self._do_retirar, args=(qtd, motivo, resp, projeto), daemon=True).start()
        except Exception as ex:
            # show on main thread
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao iniciar retirada:\n{ex}', 'Erro'))
            except Exception:
                safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao iniciar retirada:\n{ex}', 'Erro')

    def _do_retirar(self, qtd, motivo, resp, projeto=None):
        try:
            reagente_id = self.reagente_vals[0]
            self.controller.retirar_reagente(reagente_id, qtd, motivo, resp, projeto)
            # Notify on main thread
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", 'Retirada realizada com sucesso.', 'Sucesso'))
            except Exception:
                try:
                    safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", 'Retirada realizada com sucesso.', 'Sucesso')
                except Exception:
                    pass
            try:
                if callable(self.on_done):
                    self.janela.after(0, self.on_done)
            except Exception:
                pass
            try:
                self.janela.after(0, self.janela.destroy)
            except Exception:
                try:
                    self.janela.destroy()
                except Exception:
                    pass
        except Exception as ex:
            # Error on main thread
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao retirar reagente:\n{ex}', 'Erro'))
            except Exception:
                try:
                    safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao retirar reagente:\n{ex}', 'Erro')
                except Exception:
                    print('Erro ao retirar reagente:', ex)
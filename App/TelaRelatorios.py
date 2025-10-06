import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
import threading
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from ui_helpers import safe_messagebox

class TelaRelatorios:
    def __init__(self, master, controller, on_done=None):
        self.controller = controller
        self.on_done = on_done
        self.janela = ttk.Toplevel(master)
        self.janela.title('Relatórios de Movimentações')
        self.janela.transient(master)


        body = ttk.Frame(self.janela, padding=12)
        body.pack(fill='both', expand=True)

        ttk.Label(body, text='Data início (YYYY-MM-DD):').grid(row=0, column=0, sticky='w')
        self.entry_inicio = ttk.Entry(body, width=20)
        self.entry_inicio.grid(row=0, column=1, sticky='ew')

        ttk.Label(body, text='Data fim (YYYY-MM-DD):').grid(row=1, column=0, sticky='w')
        self.entry_fim = ttk.Entry(body, width=20)
        self.entry_fim.grid(row=1, column=1, sticky='ew')

        btns = ttk.Frame(body)
        btns.grid(row=2, column=0, columnspan=2, pady=(12,0))

        ttk.Button(btns, text='Gerar PDF', bootstyle='success', command=self.gerar_pdf).pack(side='left', padx=6)
        ttk.Button(btns, text='Cancelar', command=self.janela.destroy).pack(side='left', padx=6)

        body.grid_columnconfigure(1, weight=1)

    def gerar_pdf(self):
        inicio = self.entry_inicio.get().strip()
        fim = self.entry_fim.get().strip()
        if not inicio or not fim:
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "warning", 'Informe data início e fim', 'Atenção')
            return
        try:
            # validação básica de formato
            datetime.strptime(inicio[:10], '%Y-%m-%d')
            datetime.strptime(fim[:10], '%Y-%m-%d')
        except Exception:
            safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", 'Formato de data inválido. Use YYYY-MM-DD', 'Erro')
            return

        threading.Thread(target=self._gerar_pdf_thread, args=(inicio, fim), daemon=True).start()

    def _gerar_pdf_thread(self, inicio, fim):
        try:
            rows = self.controller.listar_movimentacoes_periodo(inicio, fim)
        except Exception as ex:
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao buscar movimentações:\n{ex}', 'Erro'))
            except Exception:
                safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao buscar movimentações:\n{ex}', 'Erro')
            return

        # diálogo para salvar arquivo (usar filedialog do Tk)
        try:
            # ask file destination on main thread because filedialog must run in GUI thread
            dest_container = {'dest': None}

            def ask_dest():
                from tkinter import filedialog
                sugest = f"relatorio_movimentacoes_{inicio.replace('-','')}_{fim.replace('-','')}.pdf"
                d = filedialog.asksaveasfilename(defaultextension='.pdf', initialfile=sugest, filetypes=[('PDF','*.pdf')])
                dest_container['dest'] = d

            try:
                self.janela.after(0, ask_dest)
                # wait for the dialog result by polling
                import time
                while dest_container['dest'] is None:
                    time.sleep(0.05)
            except Exception:
                # fallback: try to call directly (may fail if not main thread)
                from tkinter import filedialog
                sugest = f"relatorio_movimentacoes_{inicio.replace('-','')}_{fim.replace('-','')}.pdf"
                dest_container['dest'] = filedialog.asksaveasfilename(defaultextension='.pdf', initialfile=sugest, filetypes=[('PDF','*.pdf')])

            dest = dest_container['dest']
            if not dest:
                return
        except Exception as ex:
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao abrir diálogo de salvar:\n{ex}', 'Erro'))
            except Exception:
                safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao abrir diálogo de salvar:\n{ex}', 'Erro')
            return

        try:
            c = canvas.Canvas(dest, pagesize=A4)
            width, height = A4
            x = 40
            y = height - 40
            c.setFont('Helvetica-Bold', 14)
            c.drawString(x, y, f'Relatório de Movimentações: {inicio} a {fim}')
            y -= 30
            c.setFont('Helvetica', 10)
            for row in rows:
                # FORMATO DA LINHA (Id, Reagente_Id, Tipo, QuantidadeMovimentada, Motivo, Responsavel, Projeto, DataHora)
                linha = f"{row[7]} | Reagente:{row[1]} | Tipo:{row[2]} | Quantidade:{row[3] or ''} | Motivo:{row[4] or ''} | Resp:{row[5] or ''} | Projeto:{row[6] or ''}"
                c.drawString(x, y, linha)
                y -= 14
                if y < 60:
                    c.showPage()
                    y = height - 40
            c.save()
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", f'PDF salvo em: {dest}', 'Sucesso'))
            except Exception:
                safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "info", f'PDF salvo em: {dest}', 'Sucesso')
        except Exception as ex:
            try:
                self.janela.after(0, lambda: safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao gerar PDF:\n{ex}', 'Erro'))
            except Exception:
                safe_messagebox(self.janela if hasattr(self, 'janela') else (self.master if hasattr(self, 'master') else None), "error", f'Erro ao gerar PDF:\n{ex}', 'Erro')
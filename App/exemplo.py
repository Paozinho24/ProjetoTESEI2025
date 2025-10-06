import tkinter as tk
import ttkbootstrap as ttk
from tkinter import PhotoImage, messagebox
import sys
import os

class AppImagemContainer(tk.Tk):
    """
    Aplicação simples para demonstrar como carregar uma imagem
    e inseri-la dentro de um container (ttk.Frame) no Tkinter.
    """
    def __init__(self):
        super().__init__()
        self.title("Imagem em um Container Tkinter")
        self.geometry("500x400")
        self.style = ttk.Style(theme="litera") # Usa um tema ttkbootstrap

        # ----------------------------------------------------
        # 1. CARREGAMENTO DA IMAGEM
        # ----------------------------------------------------
        # O objeto PhotoImage DEVE ser mantido como atributo da instância (self.imagem)
        # para evitar que seja apagado pelo coletor de lixo do Python.
        
        # O arquivo 'minha_imagem.png' é o placeholder.
        self.imagem = None 
        caminho_imagem = "minha_imagem.png"

        if not os.path.exists(caminho_imagem):
            messagebox.showwarning("Aviso", f"Arquivo '{caminho_imagem}' não encontrado. Exibindo apenas texto.")
        else:
            try:
                self.imagem = PhotoImage(file=caminho_imagem)
            except tk.TclError as e:
                messagebox.showerror("Erro de Imagem", f"Não foi possível carregar a imagem. Verifique o formato (use PNG ou GIF).\nErro: {e}")

        # ----------------------------------------------------
        # 2. CRIAÇÃO DO CONTAINER (ttk.Frame)
        # ----------------------------------------------------
        # O 'container_frame' é o nosso container principal que irá agrupar a imagem.
        container_frame = ttk.Frame(self, 
                                    padding=20, 
                                    relief="raised", # Borda em relevo para destacar o container
                                    bootstyle="primary") 
        container_frame.pack(pady=50, padx=20, fill='both', expand=True)
        
        ttk.Label(container_frame, text="Este é o CONTAINER (ttk.Frame)", bootstyle="inverse-primary").pack(pady=5)

        # ----------------------------------------------------
        # 3. CRIAÇÃO E INSERÇÃO DO ELEMENTO (ttk.Label com Imagem)
        # ----------------------------------------------------
        
        # O Label é o widget que realmente pode exibir a imagem.
        # Ele é filho do container_frame.
        label_imagem = ttk.Label(container_frame, text="Espaço da Imagem")
        
        if self.imagem:
            # Associa a imagem ao Label. O Label agora "contém" a imagem.
            label_imagem.config(image=self.imagem, text="")
        
        label_imagem.pack(padx=10, pady=10) # Empacota o Label dentro do Frame

        # ----------------------------------------------------
        # 4. Exemplo de outro elemento no mesmo container
        # ----------------------------------------------------
        ttk.Button(container_frame, text="Botão Dentro do Container").pack(pady=10)


if __name__ == '__main__':
    try:
        app = AppImagemContainer()
        app.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro: {e}", file=sys.stderr)

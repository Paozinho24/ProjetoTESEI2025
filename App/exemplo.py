import tkinter as tk
from tkinter import messagebox
import sys

# Função que demonstra a messagebox de informação (showinfo)
def mostrar_mensagem():
    """
    Demonstra a tkinter.messagebox.showinfo.
    Esta função exibe um diálogo simples com ícone de informação e um botão OK.
    
    Parâmetros:
    - title: Título da janela.
    - message: Mensagem exibida no corpo.
    """
    
    # Chamada da messagebox padrão showinfo
    messagebox.showinfo(
        title="Aviso Simples",
        message="Esta é apenas uma mensagem de informação."
    )

    # Atualiza o rótulo após o diálogo ser fechado (clicando em OK)
    resultado.set("Mensagem de informação exibida e diálogo fechada.")

# NOVO: Função que demonstra um uso prático de decisão (askyesno)
def perguntar_salvar():
    """
    Demonstra a tkinter.messagebox.askyesno para confirmar uma ação crítica.
    O retorno é True (Sim) ou False (Não).
    """
    
    # 1. Abre a caixa de diálogo de Sim/Não
    resposta = messagebox.askyesno(
        title="Confirmação de Salvamento",
        message="Deseja salvar as alterações feitas no reagente antes de fechar?"
    )
    
    # 2. Testa o valor booleano retornado
    if resposta: # True se o usuário clicou em 'Sim'
        # A linha de messagebox.showinfo foi removida. O feedback agora é apenas no rótulo.
        resultado.set("Ação crítica: SIM (True). Dados salvos.")
    else: # False se o usuário clicou em 'Não'
        # Avisa que a operação foi cancelada
        messagebox.showwarning("Cancelado", "As alterações foram descartadas.")
        resultado.set("Ação crítica: NÃO (False). Alterações descartadas.")


# --- Configuração da Janela Principal ---
# Cria a janela principal do Tkinter
root = tk.Tk()
root.title("Exemplo Tkinter Messagebox Padrão (Decisão e Informação)")
root.geometry("450x200")

# Variável para exibir o resultado da interação
resultado = tk.StringVar(value="Clique em um dos botões para iniciar o diálogo.")

# Rótulo para exibir o resultado
label_resultado = tk.Label(root, textvariable=resultado, wraplength=400, pady=10)
label_resultado.pack(pady=10)

# Botão que chama a função com a messagebox showinfo
btn_info = tk.Button(
    root, 
    text="1. Mostrar Mensagem Simples (showinfo)", 
    command=mostrar_mensagem,
    padx=10, 
    pady=5
)
btn_info.pack(pady=5)

# Botão que chama a função com a messagebox askyesno (aplicação prática)
btn_decisao = tk.Button(
    root, 
    text="2. Abrir Diálogo de Decisão (askyesno)", 
    command=perguntar_salvar,
    padx=10, 
    pady=5
)
btn_decisao.pack(pady=5)


# Inicia o loop principal do Tkinter
if __name__ == '__main__':
    root.mainloop()

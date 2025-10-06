
import threading
try:
    # ttkbootstrap Messagebox
    from ttkbootstrap.dialogs import Messagebox
except Exception:
    # Fallback to tkinter messagebox (shouldn't happen if ttkbootstrap is present)
    from tkinter import messagebox as Messagebox

def _call_dialog(kind, msg, title, parent):
    # Try to bring parent to front
    try:
        if parent is not None:
            try:
                parent.lift()
            except Exception:
                pass
            try:
                parent.focus_force()
            except Exception:
                pass
            # If there is a grab somewhere, release to avoid "invisible" dialog
            try:
                parent.grab_release()
            except Exception:
                pass
    except Exception:
        pass

    if kind == "info":
        Messagebox.show_info(message=msg, title=title, parent=parent)
    elif kind == "warning":
        Messagebox.show_warning(message=msg, title=title, parent=parent)
    elif kind == "error":
        Messagebox.show_error(message=msg, title=title, parent=parent)
    else:
        # default
        Messagebox.show_info(message=msg, title=title, parent=parent)

def safe_messagebox(parent, kind, msg, title=""):
    """
    Exibe Messagebox SEMPRE no main thread, com parent visível (se disponível).
    kind: "info" | "warning" | "error"
    """
    # Escolher um parent utilizável
    # Se o parent for invisível ou destruído, tente achar um .master visível
    try:
        if parent is None and hasattr(Messagebox, "master"):
            parent = getattr(Messagebox, "master", None)
    except Exception:
        pass

    def runner():
        try:
            _call_dialog(kind, msg, title, parent)
        except Exception:
            # fallback sem parent
            _call_dialog(kind, msg, title, None)

    # Já estamos no main-thread?
    if threading.current_thread() is threading.main_thread():
        try:
            # Se existir .after no parent, usa para garantir ordem no loop
            if parent is not None and hasattr(parent, "after"):
                parent.after(0, runner)
                return
        except Exception:
            pass
        # Sem after/parent: chama direto
        runner()
    else:
        # Thread secundária: voltar ao main usando after do parent se possível
        if parent is not None and hasattr(parent, "after"):
            parent.after(0, runner)
        else:
            # Como último recurso (sem parent): tenta chamar assim mesmo
            runner()

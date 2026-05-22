"""
SGP - Widgets reutilizables
"""
import tkinter as tk
from tkinter import ttk
from frontend.styles import *


def aplicar_tema_treeview(style: ttk.Style) -> None:
    style.theme_use("clam")
    style.configure("Treeview",
                     background=TREE_BG, foreground=TREE_FG,
                     fieldbackground=TREE_BG, rowheight=26,
                     font=FONT_LABEL)
    style.configure("Treeview.Heading",
                     background=NAVY_LIGHT, foreground=GOLD,
                     font=FONT_BTN, relief="flat")
    style.map("Treeview",
              background=[("selected", TREE_SELECT)],
              foreground=[("selected", WHITE)])
    style.configure("Scrollbar",
                     background=NAVY_MED, troughcolor=NAVY,
                     arrowcolor=ICE, bordercolor=NAVY)


def frame_card(parent, **kw) -> tk.Frame:
    """Panel con estilo tarjeta oscura."""
    kw.setdefault("bg", NAVY_MED)
    kw.setdefault("padx", 12)
    kw.setdefault("pady", 10)
    return tk.Frame(parent, **kw)


def label_title(parent, text: str, **kw) -> tk.Label:
    kw.setdefault("bg", NAVY_MED)
    kw.setdefault("fg", GOLD)
    kw.setdefault("font", FONT_HEADER)
    return tk.Label(parent, text=text, **kw)


def label_body(parent, text: str, **kw) -> tk.Label:
    kw.setdefault("bg", NAVY_MED)
    kw.setdefault("fg", ICE)
    kw.setdefault("font", FONT_LABEL)
    return tk.Label(parent, text=text, **kw)


def entry_field(parent, **kw) -> tk.Entry:
    kw.update(ENTRY_STYLE)
    return tk.Entry(parent, **kw)


def btn_primary(parent, text: str, command=None, **kw) -> tk.Button:
    kw.update(BTN_PRIMARY)
    return tk.Button(parent, text=text, command=command, **kw)


def btn_danger(parent, text: str, command=None, **kw) -> tk.Button:
    kw.update(BTN_DANGER)
    return tk.Button(parent, text=text, command=command, **kw)


def btn_success(parent, text: str, command=None, **kw) -> tk.Button:
    kw.update(BTN_SUCCESS)
    return tk.Button(parent, text=text, command=command, **kw)


def btn_ghost(parent, text: str, command=None, **kw) -> tk.Button:
    kw.update(BTN_GHOST)
    return tk.Button(parent, text=text, command=command, **kw)


def separador(parent, color=NAVY_LIGHT) -> tk.Frame:
    return tk.Frame(parent, bg=color, height=1)


def tabla_con_scroll(parent, columnas: list, **kw) -> tuple[ttk.Treeview, tk.Frame]:
    """Retorna (treeview, contenedor)"""
    contenedor = tk.Frame(parent, bg=NAVY_MED)
    scroll_y = tk.Scrollbar(contenedor, orient="vertical", bg=NAVY_MED)
    scroll_x = tk.Scrollbar(contenedor, orient="horizontal", bg=NAVY_MED)
    tree = ttk.Treeview(
        contenedor, columns=columnas, show="headings",
        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, **kw
    )
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)
    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)
    return tree, contenedor


def dialogo_simple(parent, titulo: str, campos: list) -> dict | None:
    """
    Diálogo modal genérico.
    campos = [("Label", "tipo", "default"), ...]  tipo: "text"|"password"|"number"|"combo:op1,op2"
    Retorna dict con valores o None si se canceló.
    """
    top = tk.Toplevel(parent)
    top.title(titulo)
    top.configure(bg=NAVY)
    top.resizable(False, False)
    top.grab_set()

    tk.Label(top, text=titulo, bg=NAVY, fg=GOLD, font=FONT_HEADER,
             pady=8).pack(fill="x", padx=20)
    tk.Frame(top, bg=NAVY_LIGHT, height=1).pack(fill="x", padx=10, pady=2)

    frame = tk.Frame(top, bg=NAVY, pady=10, padx=20)
    frame.pack(fill="both")

    entradas = {}
    for i, campo in enumerate(campos):
        label, tipo, *resto = campo
        default = resto[0] if resto else ""
        tk.Label(frame, text=label + ":", bg=NAVY, fg=ICE, font=FONT_LABEL,
                 anchor="w").grid(row=i, column=0, sticky="w", pady=4, padx=(0, 10))

        if tipo.startswith("combo:"):
            opciones = tipo.split(":")[1].split(",")
            var = tk.StringVar(value=default or opciones[0])
            w = ttk.Combobox(frame, textvariable=var, values=opciones,
                              state="readonly", width=28, font=FONT_LABEL)
            w.grid(row=i, column=1, sticky="ew", pady=4)
            entradas[label] = var
        elif tipo == "bool":
            var = tk.BooleanVar(value=bool(default))
            w = tk.Checkbutton(frame, variable=var, bg=NAVY, fg=ICE,
                                selectcolor=NAVY_LIGHT, activebackground=NAVY)
            w.grid(row=i, column=1, sticky="w", pady=4)
            entradas[label] = var
        elif tipo in ("file", "image"):
            f_frame = tk.Frame(frame, bg=NAVY)
            f_frame.grid(row=i, column=1, sticky="ew", pady=4)
            e = tk.Entry(f_frame, width=22, **ENTRY_STYLE)
            e.insert(0, str(default))
            e.pack(side="left", padx=(0, 5))
            
            def buscar_arch(ent=e):
                from tkinter import filedialog
                path = filedialog.askopenfilename(
                    title="Seleccionar Imagen",
                    filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos", "*.*")]
                )
                if path:
                    ent.delete(0, tk.END)
                    ent.insert(0, path)
            
            tk.Button(f_frame, text="📁", command=buscar_arch, bg=NAVY_LIGHT, fg=ICE,
                      relief="flat", font=FONT_SMALL).pack(side="left")
            entradas[label] = e
        else:
            show = "*" if tipo == "password" else ""
            e = tk.Entry(frame, show=show, width=30, **ENTRY_STYLE)
            e.insert(0, str(default))
            e.grid(row=i, column=1, sticky="ew", pady=4)
            entradas[label] = e

    resultado = {"ok": False}

    def confirmar():
        resultado["ok"] = True
        resultado["datos"] = {}
        for k, v in entradas.items():
            if isinstance(v, tk.Entry):
                resultado["datos"][k] = v.get()
            else:
                resultado["datos"][k] = v.get()
        top.destroy()

    def cancelar():
        top.destroy()

    btn_frame = tk.Frame(top, bg=NAVY, pady=10)
    btn_frame.pack()
    btn_success(btn_frame, "✔ Confirmar", confirmar).pack(side="left", padx=5)
    btn_danger(btn_frame, "✖ Cancelar", cancelar).pack(side="left", padx=5)

    parent.wait_window(top)
    if resultado["ok"]:
        return resultado["datos"]
    return None

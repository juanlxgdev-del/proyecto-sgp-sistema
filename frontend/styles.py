"""
SGP - Estilos y Tema Visual
Paleta: "Elegant Midnight & Indigo" - Diseño premium y moderno
"""

# ── PALETA DE COLORES ──────────────────────────────────────────────
NAVY       = "#0B0F19"   # Fondo ultra oscuro (Deep Space)
NAVY_MED   = "#161B29"   # Fondo de paneles (Dark Slate)
NAVY_LIGHT = "#23293D"   # Bordes y separadores
BLUE       = "#4F46E5"   # Indigo (Acento principal)
BLUE_LIGHT = "#6366F1"   # Indigo claro (Hover)
ICE        = "#E2E8F0"   # Texto claro / campos
WHITE      = "#F8FAFC"   # Texto principal
GOLD       = "#FACC15"   # Alertas (Yellow Gold)
RED        = "#EF4444"   # Errores (Bright Red)
GREEN      = "#10B981"   # Confirmaciones (Emerald)
GRAY_MED   = "#94A3B8"   # Textos secundarios (Slate Gray)
ORANGE     = "#F59E0B"   # Advertencias stock (Amber)

# ── FUENTES ────────────────────────────────────────────────────────
FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_LABEL  = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Cascadia Code", 10)

# ── BOTONES ────────────────────────────────────────────────────────
BTN_PRIMARY = {
    "bg": BLUE, "fg": WHITE, "font": FONT_BTN,
    "relief": "flat", "cursor": "hand2",
    "padx": 16, "pady": 8, "bd": 0
}
BTN_DANGER = {
    "bg": RED, "fg": WHITE, "font": FONT_BTN,
    "relief": "flat", "cursor": "hand2",
    "padx": 16, "pady": 8, "bd": 0
}
BTN_SUCCESS = {
    "bg": GREEN, "fg": WHITE, "font": FONT_BTN,
    "relief": "flat", "cursor": "hand2",
    "padx": 16, "pady": 8, "bd": 0
}
BTN_WARN = {
    "bg": ORANGE, "fg": WHITE, "font": FONT_BTN,
    "relief": "flat", "cursor": "hand2",
    "padx": 16, "pady": 8, "bd": 0
}
BTN_GHOST = {
    "bg": NAVY_LIGHT, "fg": ICE, "font": FONT_BTN,
    "relief": "flat", "cursor": "hand2",
    "padx": 16, "pady": 8, "bd": 0
}

# ── ENTRADAS ───────────────────────────────────────────────────────
ENTRY_STYLE = {
    "bg": "#0F172A", "fg": WHITE,
    "insertbackground": WHITE,
    "relief": "flat", "font": FONT_BODY,
    "bd": 2
}

# ── TREEVIEW (tablas) ──────────────────────────────────────────────
TREE_BG       = "#111827"
TREE_FG       = "#F3F4F6"
TREE_SELECT   = "#3730A3" # Indigo profundo para selección
TREE_HEADING  = "#1F2937"

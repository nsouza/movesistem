# src/movesystem/utils/constants.py

"""
Responsabilidade:
- Centralizar constantes usadas pela camada de views (BaseForm e forms).
- Evitar números/strings mágicos espalhados pelo código.
"""

# ============================================================
# Estados do formulário (BaseForm)
# ============================================================

STATE_INITIAL = "INITIAL"
STATE_INSERTING = "INSERTING"
STATE_EDITING = "EDITING"
STATE_VIEWING = "VIEWING"


# ============================================================
# Textos dos botões de ação (CRUD)
# ============================================================

BUTTON_TEXT_NEW = "Novo"
BUTTON_TEXT_SAVE = "Salvar"
BUTTON_TEXT_EDIT = "Editar"
BUTTON_TEXT_DELETE = "Excluir"
BUTTON_TEXT_CANCEL = "Cancelar"
BUTTON_TEXT_EXIT = "Sair"


# ============================================================
# Ícones (emojis) dos botões de ação
# ============================================================

BUTTON_ICON_NEW = "🆕"
BUTTON_ICON_SAVE = "💾"
BUTTON_ICON_EDIT = "✏️"
BUTTON_ICON_DELETE = "🗑️"
BUTTON_ICON_CANCEL = "↩️"
BUTTON_ICON_EXIT = "🚪"


# ============================================================
# Dimensões e espaçamentos (UI)
# ============================================================

ACTION_BUTTON_WIDTH = 90
ACTION_BUTTON_HEIGHT = 60
FIELD_VERTICAL_SPACING = 10
LABEL_HORIZONTAL_SPACING = 10
# src/movesystem/views/widgets/list_panel.py

"""
Responsabilidade:
- Painel de listagem reutilizável, usado pelo BaseForm.
- Nesta primeira versão, exibe uma lista simples (QListWidget).
- Futuramente será evoluído para exibir "cards" clicáveis (conforme layout definido).
"""

from __future__ import annotations

from typing import Any, Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget


class ListPanel(QWidget):
    """
    Responsabilidade:
    - Exibir uma lista de registros.
    - Emitir um sinal quando o usuário selecionar (clicar) em um item.
    """

    # Sinal emitido ao selecionar um item; envia o "record" associado
    item_selected = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._list_widget = QListWidget()
        self._list_widget.itemClicked.connect(self._on_item_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._list_widget)

    def clear(self) -> None:
        """
        Responsabilidade:
        - Remover todos os itens da lista.
        """
        self._list_widget.clear()

    def add_item(self, label_text: str, record: Any) -> None:
        """
        Responsabilidade:
        - Adicionar um item na lista, vinculando o "record" real (objeto/model).
        - label_text é o que aparece visualmente; record é o dado completo.
        """
        item = QListWidgetItem(label_text)
        item.setData(1, record)  # NOTE: role=1 (Qt.UserRole) guarda o objeto completo
        self._list_widget.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """
        Responsabilidade:
        - Recuperar o record vinculado ao item clicado e emitir o sinal.
        """
        record = item.data(1)
        self.item_selected.emit(record)
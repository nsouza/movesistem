# src/movesystem/views/widgets/list_panel.py

"""Painel reutilizável para exibir e selecionar registros em formato de tabela."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class ListPanel(QWidget):
    """Exibe registros em linhas e emite o registro associado à linha selecionada."""

    item_selected = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inicializa a tabela e conecta a seleção de linhas ao sinal do widget."""
        super().__init__(parent)

        self._table = QTableWidget(0, 1)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().hide()
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._table.itemSelectionChanged.connect(self._on_selection_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._table)

    def set_columns(self, columns: Sequence[str]) -> None:
        """Define os títulos e a quantidade de colunas da tabela."""
        self._table.clear()
        self._table.setRowCount(0)
        self._table.setColumnCount(len(columns))
        self._table.setHorizontalHeaderLabels(list(columns))
        self._table.horizontalHeader().show()

    def clear(self) -> None:
        """Remove todas as linhas sem apagar os títulos das colunas."""
        self._table.setRowCount(0)

    def add_item(self, label_text: str, record: Any) -> None:
        """Adiciona um registro em uma linha de coluna única, mantendo compatibilidade."""
        self.add_row([label_text], record)

    def add_row(self, values: Sequence[str], record: Any) -> None:
        """Adiciona uma linha e associa o registro à primeira célula."""
        if len(values) != self._table.columnCount():
            raise ValueError("A quantidade de valores deve corresponder às colunas da tabela.")

        row_index = self._table.rowCount()
        self._table.insertRow(row_index)

        for column_index, value in enumerate(values):
            item = QTableWidgetItem(value)
            if column_index == 0:
                item.setData(Qt.ItemDataRole.UserRole, record)
            self._table.setItem(row_index, column_index, item)

    def _on_selection_changed(self) -> None:
        """Emite o registro associado à primeira célula da linha selecionada."""
        row_index = self._table.currentRow()
        if row_index < 0:
            return

        first_item = self._table.item(row_index, 0)
        if first_item is not None:
            record = first_item.data(Qt.ItemDataRole.UserRole)
            self.item_selected.emit(record)
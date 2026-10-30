# src/movesystem/views/widgets/form_dialog.py

"""Dialog modal genérico para abrir qualquer formulário herdado de BaseForm."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget

from movesystem.views.base_form import BaseForm


class FormDialog(QDialog):
    """Encapsula um BaseForm em uma janela modal."""

    def __init__(
        self,
        form: BaseForm,
        title: str,
        parent: QWidget | None = None,
        width: int = 900,
        height: int = 550,
    ) -> None:
        """Monta o dialog modal e adiciona o formulário como conteúdo."""
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(width, height)

        layout = QVBoxLayout(self)
        layout.addWidget(form)

        # NOTE: padrao do BaseForm: botao Sair emite close_requested.
        form.close_requested.connect(self.close)
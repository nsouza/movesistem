# src/movesystem/main.py

"""
Responsabilidade:
- Ponto de entrada do sistema MoveSystem.
- Inicializa a aplicação Qt (QApplication) e abre a janela principal (MainWindow).
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from movesystem.views.main_form import MainWindow


def main() -> None:
    """
    Responsabilidade:
    - Criar a QApplication, instanciar a MainWindow e iniciar o loop de eventos.
    """
    # TODO: inicializar logging (movesystem.config.logging_config) antes da UI
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
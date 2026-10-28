# src/movesystem/main.py

"""
Responsabilidade:
- Ponto de entrada do sistema MoveSystem.
- Por enquanto, apenas inicializa configurações básicas (logging/settings).
- A UI (PySide6) será conectada aqui nas próximas etapas (QApplication + MainWindow).
"""

from __future__ import annotations


def main() -> None:
    """
    Responsabilidade:
    - Função principal de inicialização do sistema.
    - Futuramente: criar QApplication, abrir MainWindow, etc.
    """
    # TODO: inicializar logging (movesystem.config.logging_config)
    # TODO: inicializar QApplication (PySide6) e MainWindow
    print("MoveSystem iniciando...")


if __name__ == "__main__":
    main()
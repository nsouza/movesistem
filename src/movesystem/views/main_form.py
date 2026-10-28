# src/movesystem/views/main_form.py

"""
Responsabilidade:
- Janela principal do sistema (shell da aplicação).
- Contém o menu suspenso (MenuBar) e a área central com abas (QTabWidget).
- Cada opção de menu abre uma tela (form) dentro de uma aba.
- Se a aba já estiver aberta, apenas foca nela (não duplica).
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QLabel,
    QVBoxLayout,
)


class MainWindow(QMainWindow):
    """
    Responsabilidade:
    - Janela principal (QMainWindow) com menu e área central em abas.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("MoveSystem - RH")
        self.showMaximized()

        # Área central: abas onde os forms serão abertos
        self._tabs = QTabWidget()
        self._tabs.setTabsClosable(True)
        self._tabs.tabCloseRequested.connect(self._close_tab)
        self.setCentralWidget(self._tabs)

        self._create_menu()
        self.statusBar().showMessage("Pronto")

    def _create_menu(self) -> None:
        """
        Responsabilidade:
        - Criar a MenuBar com os menus: Sistema, Cadastros, Relatórios, Ajuda.
        - Cada ação abre uma aba (placeholder por enquanto).
        """
        menu_bar = self.menuBar()

        # Menu Sistema
        menu_sistema = menu_bar.addMenu("Sistema")
        action_sair = menu_sistema.addAction("Sair")
        action_sair.triggered.connect(self.close)

        # Menu Cadastros
        menu_cadastros = menu_bar.addMenu("Cadastros")

        action_colaborador = menu_cadastros.addAction("Colaborador")
        action_colaborador.triggered.connect(
            lambda: self._open_tab("Colaborador", "Tela de Colaborador (em construção)")
        )

        action_afastamento = menu_cadastros.addAction("Afastamento")
        action_afastamento.triggered.connect(
            lambda: self._open_tab("Afastamento", "Tela de Afastamento (em construção)")
        )

        action_juridico = menu_cadastros.addAction("Jurídico")
        action_juridico.triggered.connect(
            lambda: self._open_tab("Jurídico", "Tela de Jurídico (em construção)")
        )

        action_treinamento = menu_cadastros.addAction("Treinamento")
        action_treinamento.triggered.connect(
            lambda: self._open_tab("Treinamento", "Tela de Treinamento (em construção)")
        )

        action_restaurante = menu_cadastros.addAction("Restaurante")
        action_restaurante.triggered.connect(
            lambda: self._open_tab("Restaurante", "Tela de Restaurante (em construção)")
        )

        # Menu Relatórios (placeholder, sem itens ainda)
        menu_bar.addMenu("Relatórios")

        # Menu Ajuda
        menu_ajuda = menu_bar.addMenu("Ajuda")
        action_sobre = menu_ajuda.addAction("Sobre")
        action_sobre.triggered.connect(
            lambda: self._open_tab("Sobre", "MoveSystem - Sistema de RH")
        )

    def _open_tab(self, title: str, placeholder_text: str) -> None:
        """
        Responsabilidade:
        - Abrir uma aba com o título informado.
        - Se já existir uma aba com esse título, apenas foca nela (não duplica).
        """
        # Verifica se a aba já existe
        for index in range(self._tabs.count()):
            if self._tabs.tabText(index) == title:
                self._tabs.setCurrentIndex(index)
                return

        # TODO: Substituir o QLabel abaixo pelo form real (ex.: ColaboradorForm)
        # quando o BaseForm e os forms estiverem implementados.
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.addWidget(QLabel(placeholder_text))

        index = self._tabs.addTab(placeholder, title)
        self._tabs.setCurrentIndex(index)

    def _close_tab(self, index: int) -> None:
        """
        Responsabilidade:
        - Fechar a aba pelo índice informado.
        """
        self._tabs.removeTab(index)
# src/movesystem/views/login_form.py

"""
Responsabilidade:
- Tela de login do sistema (QDialog modal).
- Por enquanto, valida credenciais de forma fake (sem banco de dados).
- TODO: integrar com AuthService real apos criarmos a tabela de usuarios.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

# NOTE: Usuario/senha fixos apenas para teste visual. Sera removido quando
# conectarmos no AuthService real (tabela "users" no banco).
FAKE_USERNAME = "admin"
FAKE_PASSWORD = "admin"


class LoginDialog(QDialog):
    """
    Responsabilidade:
    - Exibir o formulario de login e validar as credenciais informadas.
    - Se o login for valido, aceita o dialog (QDialog.Accepted).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("MoveSystem - Login")
        self.setFixedSize(420, 380)

        self._build_ui()

    def _build_ui(self) -> None:
        """
        Responsabilidade:
        - Montar o layout visual da tela de login.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(10)

        # Titulo
        title_label = QLabel("MoveSystem - RH")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Sistema de Recursos Humanos")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 12px; color: gray;")
        main_layout.addWidget(subtitle_label)

        main_layout.addSpacing(20)

        # Campo usuario
        username_label = QLabel("Usuario:")
        main_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Digite seu usuario")
        main_layout.addWidget(self.username_input)

        main_layout.addSpacing(10)

        # Campo senha
        password_label = QLabel("Senha:")
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.password_input)

        main_layout.addSpacing(5)

        # Link "Esqueci minha senha"
        forgot_password_button = QPushButton("Esqueci minha senha?")
        forgot_password_button.setFlat(True)
        forgot_password_button.setStyleSheet("color: blue; text-align: left;")
        forgot_password_button.clicked.connect(self._on_forgot_password_clicked)
        main_layout.addWidget(forgot_password_button)

        main_layout.addSpacing(15)

        # Botoes Entrar / Cancelar
        buttons_layout = QHBoxLayout()

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self._on_login_clicked)
        buttons_layout.addWidget(self.login_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        main_layout.addLayout(buttons_layout)

        main_layout.addStretch()

        # Rodape
        footer_label = QLabel("MoveSystem v0.1.0")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("font-size: 10px; color: gray;")
        main_layout.addWidget(footer_label)

        # Enter no campo de senha tambem aciona o login
        self.password_input.returnPressed.connect(self._on_login_clicked)

    def _on_login_clicked(self) -> None:
        """
        Responsabilidade:
        - Validar as credenciais informadas (fake, por enquanto).
        - Se validas, aceita o dialog. Se invalidas, mostra mensagem de erro.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # TODO: substituir por AuthService real (consulta na tabela "users")
        if username == FAKE_USERNAME and password == FAKE_PASSWORD:
            self.accept()
        else:
            QMessageBox.warning(
                self, "Login invalido", "Usuario ou senha incorretos."
            )

    def _on_forgot_password_clicked(self) -> None:
        """
        Responsabilidade:
        - Placeholder para o fluxo de recuperacao de senha por e-mail.
        """
        # TODO: implementar fluxo real de recuperacao de senha por e-mail (Etapa futura)
        QMessageBox.information(
            self,
            "Em construcao",
            "A recuperacao de senha por e-mail sera implementada em breve.",
        )
# src/movesystem/views/base_form.py

"""
Responsabilidade:
- Formulario base do sistema: todos os forms de cadastro herdam desta classe.
- Centraliza: layout padrao, botoes CRUD, estados (VIEW/NEW/EDIT), validacao e mensagens.
- Subclasses implementam apenas os metodos abstratos (contrato especifico de cada cadastro).
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from movesystem.utils.constants import (
    ACTION_BUTTON_HEIGHT,
    ACTION_BUTTON_WIDTH,
    BUTTON_ICON_CANCEL,
    BUTTON_ICON_DELETE,
    BUTTON_ICON_EDIT,
    BUTTON_ICON_EXIT,
    BUTTON_ICON_NEW,
    BUTTON_ICON_SAVE,
    BUTTON_TEXT_CANCEL,
    BUTTON_TEXT_DELETE,
    BUTTON_TEXT_EDIT,
    BUTTON_TEXT_EXIT,
    BUTTON_TEXT_NEW,
    BUTTON_TEXT_SAVE,
    FIELD_VERTICAL_SPACING,
    LABEL_HORIZONTAL_SPACING,
    STATE_EDITING,
    STATE_INITIAL,
    STATE_INSERTING,
    STATE_VIEWING,
)
from movesystem.views.widgets.list_panel import ListPanel


class BaseForm(QWidget):
    """
    Responsabilidade:
    - Formulario base reutilizavel por todos os cadastros do sistema.
    """

    # Sinal emitido quando o usuario clica em "Sair"
    close_requested = Signal()

    # Sobrescrito pela subclasse (titulo exibido no topo do formulario)
    title = ""

    def __init__(self, service, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.service = service
        self.state = STATE_INITIAL
        self._current_record = None

        # Registro de campos editaveis (para habilitar/desabilitar por estado)
        self._text_fields: list = []
        self._select_fields: list = []

        self._build_ui()
        self.build_fields()
        self.set_state(STATE_INITIAL)
        self.reload_list()

    # ============================================================
    # Construcao de layout (generico)
    # ============================================================

    def _build_ui(self) -> None:
        """
        Responsabilidade:
        - Montar a estrutura visual padrao: titulo, area de busca, campos,
          painel de listagem e barra de botoes.
        """
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Titulo
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Area superior (suporta coluna lateral, se a subclasse precisar)
        self.top_container = QWidget()
        self.top_layout = QHBoxLayout(self.top_container)
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        # Area de busca (linha horizontal)
        self.search_area = QWidget()
        self.search_layout = QHBoxLayout(self.search_area)
        self.search_layout.setContentsMargins(0, 0, 0, 0)
        self.search_layout.setSpacing(LABEL_HORIZONTAL_SPACING)
        self.left_layout.addWidget(self.search_area)

        # Area de campos (label a esquerda, campo a direita)
        self.fields_area = QWidget()
        self.fields_layout = QFormLayout(self.fields_area)
        self.fields_layout.setContentsMargins(0, 0, 0, 0)
        self.fields_layout.setSpacing(FIELD_VERTICAL_SPACING)
        self.fields_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.fields_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        self.left_layout.addWidget(self.fields_area)

        self.top_layout.addWidget(self.left_container)
        self.top_layout.addStretch()

        self.main_layout.addWidget(self.top_container)

        # Painel de listagem (clique no item carrega o registro)
        self.list_panel = ListPanel()
        self.list_panel.item_selected.connect(self._on_item_selected)
        self.main_layout.addWidget(self.list_panel, stretch=1)

        # Barra de botoes CRUD
        self._build_buttons()

    def _build_buttons(self) -> None:
        """
        Responsabilidade:
        - Criar a barra de botoes padrao: Novo, Salvar, Editar, Excluir, Cancelar, Sair.
        """
        self.buttons_frame = QFrame()
        self.buttons_layout = QHBoxLayout(self.buttons_frame)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(10)

        self.new_button = self._create_action_button(BUTTON_ICON_NEW, BUTTON_TEXT_NEW, self.new)
        self.buttons_layout.addWidget(self.new_button)

        self.save_button = self._create_action_button(BUTTON_ICON_SAVE, BUTTON_TEXT_SAVE, self.save)
        self.buttons_layout.addWidget(self.save_button)

        self.edit_button = self._create_action_button(BUTTON_ICON_EDIT, BUTTON_TEXT_EDIT, self.edit)
        self.buttons_layout.addWidget(self.edit_button)

        self.delete_button = self._create_action_button(
            BUTTON_ICON_DELETE, BUTTON_TEXT_DELETE, self.delete
        )
        self.buttons_layout.addWidget(self.delete_button)

        self.cancel_button = self._create_action_button(
            BUTTON_ICON_CANCEL, BUTTON_TEXT_CANCEL, self.cancel
        )
        self.buttons_layout.addWidget(self.cancel_button)

        self.buttons_layout.addStretch()

        self.exit_button = self._create_action_button(
            BUTTON_ICON_EXIT, BUTTON_TEXT_EXIT, self.close_form
        )
        self.buttons_layout.addWidget(self.exit_button)

        self.main_layout.addWidget(self.buttons_frame)

    def _create_action_button(self, icon: str, text: str, callback) -> QPushButton:
        """
        Responsabilidade:
        - Criar um botao de acao padronizado (icone + texto + tamanho fixo).
        """
        button = QPushButton(f"{icon}\n{text}")
        button.setFixedSize(ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT)
        button.clicked.connect(callback)
        return button

    # ============================================================
    # API para subclasses
    # ============================================================

    def add_search_widget(self, widget: QWidget) -> None:
        """Adiciona um widget na area de busca."""
        self.search_layout.addWidget(widget)

    def add_search_stretch(self) -> None:
        """Adiciona espacador no fim da area de busca."""
        self.search_layout.addStretch()

    def register_text_field(self, widget) -> None:
        """Registra um campo de texto para ser habilitado/desabilitado por estado."""
        self._text_fields.append(widget)

    def register_select_field(self, widget) -> None:
        """Registra um campo de selecao (combo) para ser habilitado/desabilitado por estado."""
        self._select_fields.append(widget)

    # ============================================================
    # Listagem
    # ============================================================

    def reload_list(self) -> None:
        """
        Responsabilidade:
        - Recarregar a listagem (ListPanel).
        - Implementacao padrao vazia; subclasses tipicamente sobrescrevem
          chamando self.service e depois self.list_panel.add_item(...).
        """
        pass

    def _on_item_selected(self, record) -> None:
        """
        Responsabilidade:
        - Callback chamado quando o usuario clica em um item da listagem.
        - Carrega o registro nos campos e muda o estado para VIEWING.
        """
        self._current_record = record
        self.populate_fields(record)
        self.set_state(STATE_VIEWING)

    # ============================================================
    # Metodos abstratos - subclasse DEVE implementar
    # ============================================================

    def build_fields(self) -> None:
        raise NotImplementedError

    def get_data(self) -> dict:
        raise NotImplementedError

    def populate_fields(self, record) -> None:
        raise NotImplementedError

    def clear_fields(self) -> None:
        raise NotImplementedError

    def find_record(self, value):
        raise NotImplementedError

    def get_search_value(self) -> str:
        raise NotImplementedError

    # ============================================================
    # Estados
    # ============================================================

    def set_state(self, new_state: str) -> None:
        """
        Responsabilidade:
        - Aplicar o estado atual do formulario, habilitando/desabilitando
          campos e botoes de acordo com a regra de negocio padrao.
        """
        self.state = new_state

        is_editable = new_state in (STATE_INSERTING, STATE_EDITING)

        for widget in self._text_fields:
            widget.setReadOnly(not is_editable)

        for widget in self._select_fields:
            widget.setEnabled(is_editable)

        self.save_button.setEnabled(is_editable)
        self.edit_button.setEnabled(new_state == STATE_VIEWING)
        self.delete_button.setEnabled(new_state == STATE_VIEWING)

    # ============================================================
    # Acoes genericas
    # ============================================================

    def new(self) -> None:
        """Inicia a inclusao de um novo registro."""
        self.set_state(STATE_INSERTING)
        self.clear_fields()
        self._current_record = None

    def cancel(self) -> None:
        """Cancela a operacao atual e volta ao estado inicial."""
        self.set_state(STATE_INITIAL)
        self.clear_fields()
        self._current_record = None

    def edit(self) -> None:
        """Inicia a edicao do registro atualmente carregado."""
        if self.state != STATE_VIEWING:
            QMessageBox.information(
                self, "Nada para editar", "Selecione um registro antes de clicar em Editar."
            )
            return
        self.set_state(STATE_EDITING)

    def search(self) -> None:
        """Busca um registro pelo valor informado em get_search_value()."""
        value = self.get_search_value()

        if not value:
            QMessageBox.warning(self, "Campo obrigatorio", "Digite um valor para buscar.")
            return

        record = self.find_record(value)

        if record is None:
            QMessageBox.information(
                self, "Nao encontrado", f"Nenhum registro encontrado para '{value}'."
            )
            return

        self._current_record = record
        self.populate_fields(record)
        self.set_state(STATE_VIEWING)

    def save(self) -> None:
        """Valida e persiste o registro (criacao ou atualizacao)."""
        if not self.validate():
            return

        data = self.get_data()

        try:
            if self.state == STATE_EDITING:
                record_id = self.get_current_id()
                self.service.update(record_id, data)
            else:
                self.service.save(data)
        except IntegrityError as error:
            # NOTE: SQLAlchemy encapsula violacoes de constraint (unique, FK, etc.) aqui.
            QMessageBox.warning(
                self,
                "Registro duplicado ou invalido",
                "Nao foi possivel salvar. Verifique se ha valores duplicados "
                "ou campos obrigatorios ausentes.",
            )
            # TODO: registrar log detalhado do erro (movesystem.utils.logger)
            return
        except Exception:
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                "Ocorreu um erro inesperado ao salvar. Consulte o log para mais detalhes.",
            )
            # TODO: registrar log detalhado do erro (movesystem.utils.logger)
            return

        self.set_state(STATE_INITIAL)
        self.clear_fields()
        self._current_record = None
        self.reload_list()

    def delete(self) -> None:
        """Exclui o registro atualmente carregado, apos confirmacao."""
        if self.state != STATE_VIEWING or self._current_record is None:
            QMessageBox.information(
                self, "Nada para excluir", "Selecione um registro antes de clicar em Excluir."
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirmacao",
            "Tem certeza que deseja excluir este registro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        record_id = self.get_current_id()
        self.service.delete(record_id)

        self.set_state(STATE_INITIAL)
        self.clear_fields()
        self._current_record = None
        self.reload_list()

    def close_form(self) -> None:
        """Emite o sinal de fechamento; quem abriu o form decide o que fazer."""
        self.close_requested.emit()

    # ============================================================
    # Hooks opcionais
    # ============================================================

    def validate(self) -> bool:
        """Hook de validacao; subclasses sobrescrevem quando necessario."""
        return True

    def get_current_id(self):
        """
        Responsabilidade:
        - Retornar o ID do registro atualmente carregado.
        - Assume que o record e um objeto SQLAlchemy (model) com atributo .id.
        """
        if self._current_record is None:
            return None
        return self._current_record.id
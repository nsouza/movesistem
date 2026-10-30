# src/movesystem/views/forms/team_member_form.py

"""Interface do formulário de cadastro de colaboradores."""

from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from movesystem.views.base_form import BaseForm

from movesystem.config.supervisors_config import SUPERVISORS



class TeamMemberForm(BaseForm):
    """Apresenta os campos e a lista do cadastro de colaboradores."""

    title = "Cadastro de Colaboradores"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inicializa o formulário e define o título da janela de teste isolado."""
        super().__init__(service=None, parent=parent)
        self.setWindowTitle("MoveSystem v2.0")

    def build_fields(self) -> None:
        """Cria a busca, os campos em duas colunas e as opções do formulário."""
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome ou registro...")
        self.search_input.setMinimumWidth(520)
        self.search_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.add_search_widget(self.search_input)

        search_button = QPushButton("🔍 Pesquisar")
        self.add_search_widget(search_button)
        self.add_search_stretch()

        self.register_input = QLineEdit()
        self.register_input.setInputMask("000.000/0;_")
        self.register_text_field(self.register_input)

        self.name_input = QLineEdit()
        self.register_text_field(self.name_input)

        self.cost_center_input = QLineEdit()
        self.cost_center_input.setInputMask("000.0;_")
        self.register_text_field(self.cost_center_input)

        self.supervisor_combo = QComboBox()
        self.supervisor_combo.addItem("Selecione um supervisor...", None)
        self.register_select_field(self.supervisor_combo)

        for structure_number, supervisor_name in SUPERVISORS:
            self.supervisor_combo.addItem(supervisor_name, structure_number)

        self.register_select_field(self.supervisor_combo)

        self.email_input = QLineEdit()
        self.register_text_field(self.email_input)

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDisplayFormat("dd/MM/yyyy")
        self.birth_date_input.setDate(QDate.currentDate())
        self.register_select_field(self.birth_date_input)

        self.active_yes_checkbox = QCheckBox("Sim")
        self.active_no_checkbox = QCheckBox("Não")

        self.active_options_group = QButtonGroup(self)
        self.active_options_group.setExclusive(True)
        self.active_options_group.addButton(self.active_yes_checkbox)
        self.active_options_group.addButton(self.active_no_checkbox)
        self.active_yes_checkbox.setChecked(True)

        self.register_select_field(self.active_yes_checkbox)
        self.register_select_field(self.active_no_checkbox)

        fields_grid = self._create_fields_grid()
        self.fields_layout.addRow(fields_grid)

        self.fields_area.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.left_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.top_layout.setStretch(0, 1)

        self.list_panel.set_columns(
            ["Registro", "Nome Colaborador", "C.C", "Supervisor"]
        )

    def get_data(self) -> dict:
        """Retorna os valores limpos dos campos, preparados para futura persistência."""
        return {
            "register": (
                self.register_input.text()
                .replace(".", "")
                .replace("/", "")
                .replace("_", "")
                .strip()
            ),
            "name": self.name_input.text().strip(),
            "cost_center": (
                self.cost_center_input.text().replace(".", "").replace("_", "").strip()
            ),
            "supervisor_structure": self.supervisor_combo.currentData(),
            "email": self.email_input.text().strip(),
            "date_of_birth": self.birth_date_input.date().toPython(),
            "is_active": self.active_yes_checkbox.isChecked(),
        }

    def populate_fields(self, record) -> None:
        """Preenche os campos a partir de um registro recebido."""
        self.register_input.setText(record.register)
        self.name_input.setText(record.name)
        self.cost_center_input.setText(record.cost_center)
        self.supervisor_combo.setCurrentIndex(
            self.supervisor_combo.findData(record.supervisor_structure)
        )
        self.email_input.setText(record.email)
        self.birth_date_input.setDate(
            QDate(
                record.date_of_birth.year,
                record.date_of_birth.month,
                record.date_of_birth.day,
            )
        )
        self.active_yes_checkbox.setChecked(record.is_active)
        self.active_no_checkbox.setChecked(not record.is_active)

    def clear_fields(self) -> None:
        """Limpa os campos e inicia um novo cadastro com Ativo marcado como Sim."""
        self.register_input.clear()
        self.name_input.clear()
        self.cost_center_input.clear()
        self.supervisor_combo.setCurrentIndex(0)
        self.email_input.clear()
        self.birth_date_input.setDate(QDate.currentDate())
        self.active_yes_checkbox.setChecked(True)

    def find_record(self, value):
        """Reserva a busca para a futura integração com o serviço."""
        return None

    def get_search_value(self) -> str:
        """Retorna o texto digitado no campo de busca."""
        return self.search_input.text().strip()

    def reload_list(self) -> None:
        """Limpa a lista, que será preenchida após a integração com a persistência."""
        self.list_panel.clear()

    def _create_fields_grid(self) -> QWidget:
        """Monta os campos em duas colunas e distribui o espaço disponível."""
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(12)
        grid_layout.setVerticalSpacing(12)

        grid_layout.addWidget(QLabel("Registro:"), 0, 0)
        grid_layout.addWidget(self.register_input, 0, 1)
        grid_layout.addWidget(QLabel("Nome Colaborador:"), 0, 2)
        grid_layout.addWidget(self.name_input, 0, 3)

        grid_layout.addWidget(QLabel("C.C:"), 1, 0)
        grid_layout.addWidget(self.cost_center_input, 1, 1)
        grid_layout.addWidget(QLabel("Supervisor:"), 1, 2)
        grid_layout.addWidget(self.supervisor_combo, 1, 3)

        grid_layout.addWidget(QLabel("E-mail:"), 2, 0)
        grid_layout.addWidget(self.email_input, 2, 1, 1, 3)

        grid_layout.addWidget(QLabel("Data de Nascimento:"), 3, 0)
        grid_layout.addWidget(self.birth_date_input, 3, 1)
        grid_layout.addWidget(QLabel("Ativo:"), 3, 2)

        active_options_widget = QWidget()
        active_options_layout = QHBoxLayout(active_options_widget)
        active_options_layout.setContentsMargins(0, 0, 0, 0)
        active_options_layout.addWidget(self.active_yes_checkbox)
        active_options_layout.addWidget(self.active_no_checkbox)
        active_options_layout.addStretch()
        grid_layout.addWidget(active_options_widget, 3, 3)

        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 2)

        return grid_widget
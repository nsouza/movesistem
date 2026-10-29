# src/movesystem/views/forms/test_form.py

"""
Responsabilidade:
- Form minimo apenas para validar visualmente o BaseForm (titulo, campos,
  lista, botoes e estados), sem depender de banco de dados real.
- NOTE: este arquivo e temporario; sera removido quando tivermos o primeiro
  cadastro real (ex.: Colaborador) usando Service + Repository de verdade.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QLineEdit, QPushButton

from movesystem.views.base_form import BaseForm


@dataclass
class FakeRecord:
    """Registro fake apenas para teste visual do BaseForm."""

    id: int
    name: str


class FakeService:
    """
    Responsabilidade:
    - Simular um Service real em memoria, apenas para teste do BaseForm.
    """

    def __init__(self) -> None:
        self._records: list[FakeRecord] = []
        self._next_id = 1

    def save(self, data: dict) -> FakeRecord:
        record = FakeRecord(id=self._next_id, name=data["name"])
        self._records.append(record)
        self._next_id += 1
        return record

    def update(self, record_id: int, data: dict) -> None:
        for record in self._records:
            if record.id == record_id:
                record.name = data["name"]
                return

    def delete(self, record_id: int) -> None:
        self._records = [r for r in self._records if r.id != record_id]

    def list_all(self) -> list[FakeRecord]:
        return self._records


class TestForm(BaseForm):
    """
    Responsabilidade:
    - Form minimo de teste: um unico campo "Nome".
    """

    title = "Teste do BaseForm"

    def build_fields(self) -> None:
        # Campo de busca (por nome)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome...")
        self.add_search_widget(self.search_input)

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search)
        self.add_search_widget(search_button)
        self.add_search_stretch()

        # Campo principal
        self.name_input = QLineEdit()
        self.register_text_field(self.name_input)
        self.fields_layout.addRow("Nome:", self.name_input)

    def get_data(self) -> dict:
        return {"name": self.name_input.text()}

    def populate_fields(self, record: FakeRecord) -> None:
        self.name_input.setText(record.name)

    def clear_fields(self) -> None:
        self.name_input.clear()

    def find_record(self, value: str):
        for record in self.service.list_all():
            if value.lower() in record.name.lower():
                return record
        return None

    def get_search_value(self) -> str:
        return self.search_input.text().strip()

    def reload_list(self) -> None:
        self.list_panel.clear()
        for record in self.service.list_all():
            self.list_panel.add_item(record.name, record)
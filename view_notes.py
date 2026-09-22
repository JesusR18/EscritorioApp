"""Vista de gestión de notas."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QListWidget, QListWidgetItem, QFrame, QTextEdit, QMessageBox
)

from database import Database, Note


class NoteEditor(QFrame):
    saved = Signal()

    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_note_id: int | None = None
        self.setObjectName("Card")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self.header = QLabel("Nueva nota")
        self.header.setObjectName("TitleLabel")
        layout.addWidget(self.header)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Título *")
        layout.addWidget(self.title_input)

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(["General", "Ideas", "Trabajo", "Personal"])
        layout.addWidget(self.category_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Escribe tu nota aquí...")
        layout.addWidget(self.content_input, 1)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("Guardar nota")
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("GhostButton")
        self.cancel_btn.clicked.connect(self.clear)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def load_note(self, note: Note):
        self.current_note_id = note.id
        self.header.setText("Editar nota")
        self.title_input.setText(note.title)
        self.category_input.setCurrentText(note.category)
        self.content_input.setPlainText(note.content)

    def clear(self):
        self.current_note_id = None
        self.header.setText("Nueva nota")
        self.title_input.clear()
        self.category_input.setCurrentText("General")
        self.content_input.clear()

    def save(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Falta información", "El título de la nota es obligatorio.")
            return
        content = self.content_input.toPlainText()
        category = self.category_input.currentText().strip() or "General"

        if self.current_note_id is None:
            self.db.add_note(title, content, category)
        else:
            self.db.update_note(self.current_note_id, title=title, content=content, category=category)
        self.clear()
        self.saved.emit()


class NotesView(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.all_notes: list[Note] = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(12)

        title = QLabel("Notas")
        title.setObjectName("TitleLabel")
        left.addWidget(title)

        filter_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar notas...")
        self.search_input.textChanged.connect(self.refresh)
        filter_row.addWidget(self.search_input, 2)

        self.filter_category = QComboBox()
        self.filter_category.addItem("Todas las categorías")
        self.filter_category.currentIndexChanged.connect(self.refresh)
        filter_row.addWidget(self.filter_category, 1)
        left.addLayout(filter_row)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        left.addWidget(self.list_widget, 1)

        actions_row = QHBoxLayout()
        self.new_btn = QPushButton("+ Nueva nota")
        self.new_btn.clicked.connect(lambda: self.editor.clear())
        self.pin_btn = QPushButton("Fijar/Desfijar")
        self.pin_btn.setObjectName("GhostButton")
        self.pin_btn.clicked.connect(self.toggle_pin_selected)
        self.delete_btn = QPushButton("Eliminar")
        self.delete_btn.setObjectName("DangerButton")
        self.delete_btn.clicked.connect(self.delete_selected)
        actions_row.addWidget(self.new_btn)
        actions_row.addWidget(self.pin_btn)
        actions_row.addWidget(self.delete_btn)
        left.addLayout(actions_row)

        root.addLayout(left, 3)

        self.editor = NoteEditor(self.db)
        self.editor.saved.connect(self.refresh)
        self.editor.setMinimumWidth(340)
        self.editor.setMaximumWidth(400)
        root.addWidget(self.editor, 2)

    def _selected_note(self) -> Note | None:
        item = self.list_widget.currentItem()
        if item is None:
            return None
        note_id = item.data(Qt.UserRole)
        return next((n for n in self.all_notes if n.id == note_id), None)

    def _on_item_clicked(self, item: QListWidgetItem):
        note_id = item.data(Qt.UserRole)
        note = next((n for n in self.all_notes if n.id == note_id), None)
        if note:
            self.editor.load_note(note)

    def toggle_pin_selected(self):
        note = self._selected_note()
        if note is None:
            QMessageBox.information(self, "Sin selección", "Selecciona una nota primero.")
            return
        self.db.update_note(note.id, pinned=0 if note.pinned else 1)
        self.refresh()

    def delete_selected(self):
        note = self._selected_note()
        if note is None:
            QMessageBox.information(self, "Sin selección", "Selecciona una nota para eliminar.")
            return
        confirm = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Eliminar la nota \"{note.title}\"?"
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_note(note.id)
            self.editor.clear()
            self.refresh()

    def refresh(self):
        self.all_notes = self.db.get_notes()

        current_cat = self.filter_category.currentText()
        self.filter_category.blockSignals(True)
        self.filter_category.clear()
        self.filter_category.addItem("Todas las categorías")
        for cat in self.db.note_categories():
            self.filter_category.addItem(cat)
        idx = self.filter_category.findText(current_cat)
        self.filter_category.setCurrentIndex(idx if idx >= 0 else 0)
        self.filter_category.blockSignals(False)

        query = self.search_input.text().strip().lower()
        cat_filter = self.filter_category.currentText()

        filtered = []
        for n in self.all_notes:
            if query and query not in n.title.lower() and query not in n.content.lower():
                continue
            if cat_filter != "Todas las categorías" and n.category != cat_filter:
                continue
            filtered.append(n)

        self.list_widget.clear()
        for n in filtered:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, n.id)
            widget = self._build_note_widget(n)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    def _build_note_widget(self, note: Note) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(8, 6, 8, 6)
        v.setSpacing(2)

        title_row = QHBoxLayout()
        prefix = "📌 " if note.pinned else ""
        title_lbl = QLabel(f"{prefix}{note.title}")
        title_lbl.setStyleSheet("font-weight: 700;")
        title_row.addWidget(title_lbl)
        title_row.addStretch()
        v.addLayout(title_row)

        preview = note.content.strip().replace("\n", " ")
        if len(preview) > 90:
            preview = preview[:90] + "..."
        preview_lbl = QLabel(preview or "(sin contenido)")
        preview_lbl.setObjectName("SubtitleLabel")
        v.addWidget(preview_lbl)

        meta_lbl = QLabel(f"{note.category} · Actualizado: {note.updated_at[:16].replace('T', ' ')}")
        meta_lbl.setObjectName("SubtitleLabel")
        v.addWidget(meta_lbl)

        return w

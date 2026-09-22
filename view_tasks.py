"""Vista de gestión de tareas."""
from __future__ import annotations

from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QListWidget, QListWidgetItem, QFrame, QDateEdit, QTextEdit,
    QMessageBox, QCheckBox, QSizePolicy
)
from PySide6.QtGui import QFont

from database import Database, Task
from styles import PRIORITY_COLORS


class TaskEditor(QFrame):
    """Panel para crear/editar una tarea."""
    saved = Signal()

    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_task_id: int | None = None
        self.setObjectName("Card")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self.header = QLabel("Nueva tarea")
        self.header.setObjectName("TitleLabel")
        layout.addWidget(self.header)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Título de la tarea *")
        layout.addWidget(self.title_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Descripción (opcional)")
        self.desc_input.setFixedHeight(80)
        layout.addWidget(self.desc_input)

        row = QHBoxLayout()
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(["General", "Trabajo", "Personal", "Estudio", "Urgente"])
        row.addWidget(self._labeled("Categoría", self.category_input))

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Baja", "Media", "Alta"])
        self.priority_input.setCurrentText("Media")
        row.addWidget(self._labeled("Prioridad", self.priority_input))
        layout.addLayout(row)

        row2 = QHBoxLayout()
        self.has_due_date = QCheckBox("Con fecha límite")
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setEnabled(False)
        self.has_due_date.toggled.connect(self.due_date_input.setEnabled)
        row2.addWidget(self.has_due_date)
        row2.addWidget(self.due_date_input)
        row2.addStretch()
        layout.addLayout(row2)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("Guardar tarea")
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("GhostButton")
        self.cancel_btn.clicked.connect(self.clear)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _labeled(self, text: str, widget: QWidget) -> QWidget:
        container = QWidget()
        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(4)
        lbl = QLabel(text)
        lbl.setObjectName("SubtitleLabel")
        v.addWidget(lbl)
        v.addWidget(widget)
        return container

    def load_task(self, task: Task):
        self.current_task_id = task.id
        self.header.setText("Editar tarea")
        self.title_input.setText(task.title)
        self.desc_input.setPlainText(task.description)
        self.category_input.setCurrentText(task.category)
        self.priority_input.setCurrentText(task.priority)
        if task.due_date:
            self.has_due_date.setChecked(True)
            self.due_date_input.setDate(QDate.fromString(task.due_date, "yyyy-MM-dd"))
        else:
            self.has_due_date.setChecked(False)

    def clear(self):
        self.current_task_id = None
        self.header.setText("Nueva tarea")
        self.title_input.clear()
        self.desc_input.clear()
        self.category_input.setCurrentText("General")
        self.priority_input.setCurrentText("Media")
        self.has_due_date.setChecked(False)
        self.due_date_input.setDate(QDate.currentDate())

    def save(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Falta información", "El título de la tarea es obligatorio.")
            return
        description = self.desc_input.toPlainText().strip()
        category = self.category_input.currentText().strip() or "General"
        priority = self.priority_input.currentText()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd") if self.has_due_date.isChecked() else ""

        if self.current_task_id is None:
            self.db.add_task(title, description, category, priority, due_date)
        else:
            self.db.update_task(
                self.current_task_id, title=title, description=description,
                category=category, priority=priority, due_date=due_date,
            )
        self.clear()
        self.saved.emit()


class TasksView(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.all_tasks: list[Task] = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(12)

        title = QLabel("Tareas")
        title.setObjectName("TitleLabel")
        left.addWidget(title)

        filter_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar tareas...")
        self.search_input.textChanged.connect(self.refresh)
        filter_row.addWidget(self.search_input, 2)

        self.filter_category = QComboBox()
        self.filter_category.addItem("Todas las categorías")
        self.filter_category.currentIndexChanged.connect(self.refresh)
        filter_row.addWidget(self.filter_category, 1)

        self.filter_status = QComboBox()
        self.filter_status.addItems(["Todas", "Pendientes", "Completadas"])
        self.filter_status.currentIndexChanged.connect(self.refresh)
        filter_row.addWidget(self.filter_status, 1)
        left.addLayout(filter_row)

        self.stats_label = QLabel()
        self.stats_label.setObjectName("SubtitleLabel")
        left.addWidget(self.stats_label)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        left.addWidget(self.list_widget, 1)

        actions_row = QHBoxLayout()
        self.new_btn = QPushButton("+ Nueva tarea")
        self.new_btn.clicked.connect(lambda: self.editor.clear())
        self.delete_btn = QPushButton("Eliminar seleccionada")
        self.delete_btn.setObjectName("DangerButton")
        self.delete_btn.clicked.connect(self.delete_selected)
        actions_row.addWidget(self.new_btn)
        actions_row.addWidget(self.delete_btn)
        left.addLayout(actions_row)

        root.addLayout(left, 3)

        self.editor = TaskEditor(self.db)
        self.editor.saved.connect(self.refresh)
        self.editor.setMinimumWidth(320)
        self.editor.setMaximumWidth(360)
        root.addWidget(self.editor, 2)

    def _selected_task(self) -> Task | None:
        item = self.list_widget.currentItem()
        if item is None:
            return None
        task_id = item.data(Qt.UserRole)
        return next((t for t in self.all_tasks if t.id == task_id), None)

    def _on_item_clicked(self, item: QListWidgetItem):
        task_id = item.data(Qt.UserRole)
        task = next((t for t in self.all_tasks if t.id == task_id), None)
        if task:
            self.editor.load_task(task)

    def toggle_complete(self, task: Task):
        self.db.update_task(task.id, completed=0 if task.completed else 1)
        self.refresh()

    def delete_selected(self):
        task = self._selected_task()
        if task is None:
            QMessageBox.information(self, "Sin selección", "Selecciona una tarea para eliminar.")
            return
        confirm = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Eliminar la tarea \"{task.title}\"?"
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_task(task.id)
            self.editor.clear()
            self.refresh()

    def refresh(self):
        self.all_tasks = self.db.get_tasks()

        current_cat = self.filter_category.currentText()
        self.filter_category.blockSignals(True)
        self.filter_category.clear()
        self.filter_category.addItem("Todas las categorías")
        for cat in self.db.task_categories():
            self.filter_category.addItem(cat)
        idx = self.filter_category.findText(current_cat)
        self.filter_category.setCurrentIndex(idx if idx >= 0 else 0)
        self.filter_category.blockSignals(False)

        query = self.search_input.text().strip().lower()
        cat_filter = self.filter_category.currentText()
        status_filter = self.filter_status.currentText()

        filtered = []
        for t in self.all_tasks:
            if query and query not in t.title.lower() and query not in t.description.lower():
                continue
            if cat_filter != "Todas las categorías" and t.category != cat_filter:
                continue
            if status_filter == "Pendientes" and t.completed:
                continue
            if status_filter == "Completadas" and not t.completed:
                continue
            filtered.append(t)

        self.list_widget.clear()
        for t in filtered:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, t.id)
            widget = self._build_task_widget(t)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

        total = len(self.all_tasks)
        done = sum(1 for t in self.all_tasks if t.completed)
        self.stats_label.setText(f"{done}/{total} tareas completadas · {total - done} pendientes")

    def _build_task_widget(self, task: Task) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(6, 4, 6, 4)

        checkbox = QCheckBox()
        checkbox.setChecked(task.completed)
        checkbox.stateChanged.connect(lambda _=None, t=task: self.toggle_complete(t))
        h.addWidget(checkbox)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title_lbl = QLabel(task.title)
        font = QFont()
        font.setStrikeOut(task.completed)
        font.setBold(True)
        title_lbl.setFont(font)
        text_col.addWidget(title_lbl)

        meta_parts = [task.category]
        if task.due_date:
            meta_parts.append(f"Vence: {task.due_date}")
        meta_lbl = QLabel(" · ".join(meta_parts))
        meta_lbl.setObjectName("SubtitleLabel")
        text_col.addWidget(meta_lbl)

        h.addLayout(text_col, 1)

        priority_lbl = QLabel(task.priority)
        color = PRIORITY_COLORS.get(task.priority, "#999")
        priority_lbl.setStyleSheet(
            f"background-color: {color}; color: white; border-radius: 8px; padding: 3px 10px; font-weight: 600;"
        )
        h.addWidget(priority_lbl)

        return w

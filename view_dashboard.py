"""Vista de panel principal con estadísticas."""
from __future__ import annotations

from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QListWidget,
    QListWidgetItem
)

from database import Database


class StatCard(QLabel):
    def __init__(self, value: str, label: str):
        super().__init__()
        self.setObjectName("StatCard")
        self.setText(f"<div style='font-size:26px;font-weight:700'>{value}</div>"
                     f"<div style='color:#8b8da0;font-size:12px'>{label}</div>")
        self.setTextFormat(Qt.RichText)


class DashboardView(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("Panel principal")
        title.setObjectName("TitleLabel")
        root.addWidget(title)

        subtitle = QLabel("Resumen de tu actividad")
        subtitle.setObjectName("SubtitleLabel")
        root.addWidget(subtitle)

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(14)
        root.addLayout(self.stats_grid)

        upcoming_title = QLabel("Próximas tareas")
        upcoming_title.setObjectName("TitleLabel")
        upcoming_title.setStyleSheet("font-size: 16px; margin-top: 10px;")
        root.addWidget(upcoming_title)

        self.upcoming_list = QListWidget()
        root.addWidget(self.upcoming_list, 1)

    def refresh(self):
        for i in reversed(range(self.stats_grid.count())):
            item = self.stats_grid.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        tasks = self.db.get_tasks()
        notes = self.db.get_notes()
        pending = [t for t in tasks if not t.completed]
        done = [t for t in tasks if t.completed]
        overdue = [
            t for t in pending
            if t.due_date and date.fromisoformat(t.due_date) < date.today()
        ]

        cards = [
            (str(len(tasks)), "Tareas totales"),
            (str(len(pending)), "Pendientes"),
            (str(len(done)), "Completadas"),
            (str(len(overdue)), "Vencidas"),
            (str(len(notes)), "Notas guardadas"),
        ]
        for i, (value, label) in enumerate(cards):
            card = StatCard(value, label)
            self.stats_grid.addWidget(card, 0, i)

        self.upcoming_list.clear()
        upcoming = sorted((t for t in pending if t.due_date), key=lambda t: t.due_date)[:8]
        if not upcoming:
            item = QListWidgetItem("No hay tareas con fecha límite próxima.")
            self.upcoming_list.addItem(item)
        for t in upcoming:
            is_overdue = date.fromisoformat(t.due_date) < date.today()
            prefix = "⚠️ VENCIDA — " if is_overdue else ""
            item = QListWidgetItem(f"{prefix}{t.title}  ·  {t.category}  ·  Vence {t.due_date}")
            self.upcoming_list.addItem(item)

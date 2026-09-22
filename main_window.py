"""Ventana principal de la aplicación."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QButtonGroup, QFrame
)
from PySide6.QtGui import QIcon

from database import Database
from styles import LIGHT_QSS, DARK_QSS
from view_dashboard import DashboardView
from view_tasks import TasksView
from view_notes import NotesView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor Personal")
        self.resize(1180, 760)
        self.setMinimumSize(900, 600)

        self.db = Database()
        self.dark_mode = self.db.get_setting("theme", "light") == "dark"

        self._build_ui()
        self.apply_theme()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---- Sidebar ----
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 20, 16, 20)
        side_layout.setSpacing(6)

        brand = QLabel("🗂️  Gestor Personal")
        brand.setStyleSheet("font-size: 16px; font-weight: 700; padding: 6px 8px 18px 8px;")
        side_layout.addWidget(brand)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.btn_dashboard = self._nav_button("🏠  Panel principal")
        self.btn_tasks = self._nav_button("✅  Tareas")
        self.btn_notes = self._nav_button("📝  Notas")

        for i, btn in enumerate([self.btn_dashboard, self.btn_tasks, self.btn_notes]):
            self.nav_group.addButton(btn, i)
            side_layout.addWidget(btn)

        self.btn_dashboard.setChecked(True)
        side_layout.addStretch()

        self.theme_btn = QPushButton("🌙  Modo oscuro")
        self.theme_btn.setObjectName("GhostButton")
        self.theme_btn.clicked.connect(self.toggle_theme)
        side_layout.addWidget(self.theme_btn)

        root.addWidget(sidebar)

        # ---- Stacked pages ----
        self.stack = QStackedWidget()
        self.dashboard_view = DashboardView(self.db)
        self.tasks_view = TasksView(self.db)
        self.notes_view = NotesView(self.db)

        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.tasks_view)
        self.stack.addWidget(self.notes_view)
        root.addWidget(self.stack, 1)

        self.nav_group.idClicked.connect(self._on_nav_changed)

    def _nav_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def _on_nav_changed(self, index: int):
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.dashboard_view.refresh()
        elif index == 1:
            self.tasks_view.refresh()
        elif index == 2:
            self.notes_view.refresh()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.db.set_setting("theme", "dark" if self.dark_mode else "light")
        self.apply_theme()

    def apply_theme(self):
        app = self.window().parent() or None
        from PySide6.QtWidgets import QApplication
        QApplication.instance().setStyleSheet(DARK_QSS if self.dark_mode else LIGHT_QSS)
        self.theme_btn.setText("☀️  Modo claro" if self.dark_mode else "🌙  Modo oscuro")

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

"""Hojas de estilo QSS para tema claro y oscuro."""

LIGHT_QSS = """
QWidget {
    background-color: #f5f6fa;
    color: #1e2028;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
QMainWindow, #Sidebar {
    background-color: #ffffff;
}
#Sidebar {
    border-right: 1px solid #e2e4ea;
}
QPushButton {
    background-color: #4f6bf0;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 600;
}
QPushButton:hover { background-color: #3d56d6; }
QPushButton:pressed { background-color: #2f45b0; }
QPushButton:disabled { background-color: #c6cbe8; }
QPushButton#NavButton {
    background-color: transparent;
    color: #4a4d5a;
    text-align: left;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 500;
}
QPushButton#NavButton:hover { background-color: #eef0fb; }
QPushButton#NavButton:checked {
    background-color: #4f6bf0;
    color: white;
}
QPushButton#DangerButton {
    background-color: #e5484d;
}
QPushButton#DangerButton:hover { background-color: #c93d42; }
QPushButton#GhostButton {
    background-color: transparent;
    color: #4f6bf0;
    border: 1px solid #c9d0f5;
    font-weight: 500;
}
QPushButton#GhostButton:hover { background-color: #eef0fb; }
QLineEdit, QTextEdit, QComboBox, QDateEdit {
    background-color: #ffffff;
    border: 1px solid #d7dae2;
    border-radius: 6px;
    padding: 6px 8px;
    selection-background-color: #4f6bf0;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #4f6bf0;
}
QListWidget {
    background-color: #ffffff;
    border: 1px solid #e2e4ea;
    border-radius: 8px;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    padding: 10px;
    border-radius: 6px;
    margin: 2px;
}
QListWidget::item:selected {
    background-color: #eef0fb;
    color: #1e2028;
}
QListWidget::item:hover { background-color: #f5f6fa; }
QLabel#TitleLabel { font-size: 20px; font-weight: 700; }
QLabel#SubtitleLabel { color: #7a7d8a; font-size: 12px; }
QLabel#StatCard {
    background-color: #ffffff;
    border: 1px solid #e2e4ea;
    border-radius: 10px;
    padding: 14px;
}
QFrame#Card {
    background-color: #ffffff;
    border: 1px solid #e2e4ea;
    border-radius: 10px;
}
QScrollBar:vertical { background: transparent; width: 10px; }
QScrollBar::handle:vertical { background: #d7dae2; border-radius: 5px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #b9bdd0; }
QCheckBox { spacing: 8px; }
QComboBox::drop-down { border: none; }
"""

DARK_QSS = """
QWidget {
    background-color: #1b1d27;
    color: #e7e8ee;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
QMainWindow, #Sidebar {
    background-color: #14151d;
}
#Sidebar {
    border-right: 1px solid #2a2c3a;
}
QPushButton {
    background-color: #6478ff;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 600;
}
QPushButton:hover { background-color: #7c8cff; }
QPushButton:pressed { background-color: #4d5edb; }
QPushButton:disabled { background-color: #3a3d55; }
QPushButton#NavButton {
    background-color: transparent;
    color: #b7b9c9;
    text-align: left;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 500;
}
QPushButton#NavButton:hover { background-color: #23253346; }
QPushButton#NavButton:checked {
    background-color: #6478ff;
    color: white;
}
QPushButton#DangerButton {
    background-color: #e5484d;
}
QPushButton#DangerButton:hover { background-color: #c93d42; }
QPushButton#GhostButton {
    background-color: transparent;
    color: #8fa0ff;
    border: 1px solid #383b57;
    font-weight: 500;
}
QPushButton#GhostButton:hover { background-color: #23253a; }
QLineEdit, QTextEdit, QComboBox, QDateEdit {
    background-color: #232533;
    border: 1px solid #34364a;
    border-radius: 6px;
    padding: 6px 8px;
    color: #e7e8ee;
    selection-background-color: #6478ff;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #6478ff;
}
QListWidget {
    background-color: #1f202c;
    border: 1px solid #2a2c3a;
    border-radius: 8px;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    padding: 10px;
    border-radius: 6px;
    margin: 2px;
}
QListWidget::item:selected {
    background-color: #2a2c47;
    color: #ffffff;
}
QListWidget::item:hover { background-color: #23253a; }
QLabel#TitleLabel { font-size: 20px; font-weight: 700; color: #ffffff; }
QLabel#SubtitleLabel { color: #8b8da0; font-size: 12px; }
QLabel#StatCard {
    background-color: #1f202c;
    border: 1px solid #2a2c3a;
    border-radius: 10px;
    padding: 14px;
}
QFrame#Card {
    background-color: #1f202c;
    border: 1px solid #2a2c3a;
    border-radius: 10px;
}
QScrollBar:vertical { background: transparent; width: 10px; }
QScrollBar::handle:vertical { background: #34364a; border-radius: 5px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #46496b; }
QCheckBox { spacing: 8px; }
QComboBox::drop-down { border: none; }
"""

PRIORITY_COLORS = {
    "Alta": "#e5484d",
    "Media": "#f5a623",
    "Baja": "#2ecc71",
}

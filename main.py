"""Punto de entrada de la aplicación de escritorio Gestor Personal."""
import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Gestor Personal.")
    app.setOrganizationName("GestorPersonal")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
"""
Kuro AI — Punto de entrada principal.

Uso:
    python main.py

La ventana aparece en el lado derecho de la pantalla.
Presiona Escape para ocultarla, F24 para toggle (requiere KDE shortcut configurado).
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from ui.window import KuroWindow
from core.settings import load as load_config


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kuro AI")
    app.setOrganizationName("hoshikokuro")

    # Fuente base
    font = QFont("JetBrainsMono Nerd Font Mono", 10)
    app.setFont(font)

    # Hoja de estilos global (scrollbars, tooltips)
    app.setStyleSheet("""
        QToolTip {
            background: rgba(10, 13, 18, 0.95);
            color: rgba(67, 210, 145, 0.9);
            border: 1px solid rgba(67, 210, 145, 0.20);
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 11px;
            font-family: 'JetBrainsMono Nerd Font Mono', monospace;
        }
    """)

    config = load_config()

    window = KuroWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

"""
Kuro AI — Punto de entrada principal.

Uso:
    python main.py

La ventana aparece en el lado derecho de la pantalla.
Presiona Escape para ocultarla, F24 para toggle (requiere KDE shortcut configurado).
"""

import sys
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

from ui.window import KuroWindow
from core.settings import load as load_config


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kuro AI")
    app.setOrganizationName("hoshikokuro")

    # Cerrar limpiamente cuando se usa Ctrl+C desde la terminal
    signal.signal(signal.SIGINT, lambda *_: app.quit())
    signal.signal(signal.SIGTERM, lambda *_: app.quit())

    # Pulso cada 200ms para que Python procese señales UNIX (Ctrl+C)
    # sin esto, el event loop de Qt bloquea las señales del SO
    pulse = QTimer()
    pulse.setInterval(200)
    pulse.timeout.connect(lambda: None)
    pulse.start()

    # Asegurar que cerrar la ventana termina el proceso
    app.setQuitOnLastWindowClosed(True)

    # Fuente base
    font = QFont("JetBrainsMono Nerd Font Mono", 10)
    app.setFont(font)

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

"""
Barra de herramientas inferior de Kuro AI.
Input de texto, botón enviar, chips de modo (web/offline/historial).
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent


class ToolChip(QPushButton):
    """Chip toggle de la barra inferior."""

    def __init__(self, text: str, icon: str = "", checkable: bool = True, parent=None):
        super().__init__(parent)
        self.setText(f"{icon}  {text}" if icon else text)
        self.setCheckable(checkable)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style(False)
        self.toggled.connect(self._update_style)

    def _update_style(self, checked: bool):
        if checked:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(67, 210, 145, 0.09);
                    border: 1px solid rgba(67, 210, 145, 0.32);
                    border-radius: 7px;
                    color: rgba(67, 210, 145, 0.9);
                    font-size: 10px;
                    padding: 3px 9px;
                    font-family: 'JetBrainsMono Nerd Font Mono', monospace;
                }
                QPushButton:hover {
                    background: rgba(67, 210, 145, 0.14);
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid rgba(255, 255, 255, 0.07);
                    border-radius: 7px;
                    color: rgba(255, 255, 255, 0.30);
                    font-size: 10px;
                    padding: 3px 9px;
                    font-family: 'JetBrainsMono Nerd Font Mono', monospace;
                }
                QPushButton:hover {
                    border-color: rgba(67, 210, 145, 0.25);
                    color: rgba(67, 210, 145, 0.65);
                }
            """)


class SendButton(QPushButton):
    """Botón de enviar con flecha."""

    def __init__(self, parent=None):
        super().__init__("→", parent)
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(67, 210, 145, 0.15);
                border: 1px solid rgba(67, 210, 145, 0.28);
                border-radius: 9px;
                color: rgba(67, 210, 145, 0.95);
                font-size: 15px;
                font-weight: 400;
            }
            QPushButton:hover {
                background: rgba(67, 210, 145, 0.28);
                border-color: rgba(67, 210, 145, 0.50);
            }
            QPushButton:pressed {
                background: rgba(67, 210, 145, 0.38);
            }
        """)


class ChatInput(QLineEdit):
    """Input de texto del chat con Enter para enviar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Escribe algo...")
        self.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.80);
                font-size: 13px;
                font-family: 'JetBrainsMono Nerd Font Mono', monospace;
                selection-background-color: rgba(67, 210, 145, 0.25);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.25);
            }
        """)


class Toolbar(QWidget):
    """
    Barra inferior completa: input + send + chips.
    Señales:
      - message_sent(str)  → cuando el usuario envía un mensaje
      - web_toggled(bool)  → cuando cambia el modo web
    """

    message_sent = pyqtSignal(str)
    web_toggled   = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 14)
        layout.setSpacing(10)

        # Fila de input
        input_row = QHBoxLayout()
        input_row.setSpacing(8)

        self._input = ChatInput()
        self._send_btn = SendButton()

        input_row.addWidget(self._input)
        input_row.addWidget(self._send_btn)

        input_container = QWidget()
        input_container.setLayout(input_row)
        input_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(67, 210, 145, 0.16);
                border-radius: 12px;
                padding: 2px 6px;
            }
        """)

        # Fila de chips
        chips_row = QHBoxLayout()
        chips_row.setSpacing(6)
        chips_row.setContentsMargins(0, 0, 0, 0)

        self._web_chip = ToolChip("web", checkable=True)
        self._web_chip.setChecked(True)

        self._history_chip = ToolChip("historial", checkable=False)

        self._model_label = QLabel("qwen2.5:7b")
        self._model_label.setStyleSheet("""
            color: rgba(255,255,255,0.18);
            font-size: 10px;
            font-family: 'JetBrainsMono Nerd Font Mono', monospace;
        """)

        chips_row.addWidget(self._web_chip)
        chips_row.addWidget(self._history_chip)
        chips_row.addStretch()
        chips_row.addWidget(self._model_label)

        layout.addWidget(input_container)
        layout.addLayout(chips_row)

        self.setStyleSheet("""
            Toolbar {
                background: rgba(0, 0, 0, 0.18);
                border-top: 1px solid rgba(67, 210, 145, 0.08);
            }
        """)

    def _connect_signals(self):
        self._send_btn.clicked.connect(self._send)
        self._input.returnPressed.connect(self._send)
        self._web_chip.toggled.connect(self._on_web_toggle)

    def _send(self):
        text = self._input.text().strip()
        if text:
            self.message_sent.emit(text)
            self._input.clear()

    def _on_web_toggle(self, checked: bool):
        self.web_toggled.emit(checked)
        self._model_label.setText(
            "qwen2.5:7b" if checked else "sin conexión"
        )

    def set_model(self, model: str):
        self._model_label.setText(model)

    def set_enabled(self, enabled: bool):
        self._input.setEnabled(enabled)
        self._send_btn.setEnabled(enabled)

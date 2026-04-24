"""
Barra de herramientas inferior de Kuro AI.
Input, enviar, chips: web, extensiones, historial, nuevo chat.
Se adapta a tema claro/oscuro del sistema.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
import ui.theme as T


class ToolChip(QPushButton):
    """
    Chip toggle/acción de la barra inferior.
    checkable=True → toggle (web on/off)
    checkable=False → acción puntual (historial, nuevo chat)
    """

    def __init__(self, text: str, checkable: bool = True, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(checkable)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style(self.isChecked())
        if checkable:
            self.toggled.connect(self._apply_style)

    def _apply_style(self, checked: bool = False):
        if self.isCheckable() and checked:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {T.chip_active_bg()};
                    border: 1px solid {T.chip_active_border()};
                    border-radius: 6px;
                    color: {T.accent(0.92)};
                    font-size: 10px;
                    padding: 3px 9px;
                }}
                QPushButton:hover {{
                    background: {T.accent(0.14)};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: 1px solid {T.chip_inactive_border()};
                    border-radius: 6px;
                    color: {T.chip_inactive_text()};
                    font-size: 10px;
                    padding: 3px 9px;
                }}
                QPushButton:hover {{
                    border-color: {T.accent(0.28)};
                    color: {T.accent(0.75)};
                }}
                QPushButton:pressed {{
                    background: {T.accent(0.08)};
                }}
            """)

    def refresh_theme(self):
        self._apply_style(self.isChecked())


class SendButton(QPushButton):
    """Botón de enviar."""

    def __init__(self, parent=None):
        super().__init__("↑", parent)
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: {T.accent(0.15)};
                border: 1px solid {T.accent(0.30)};
                border-radius: 9px;
                color: {T.accent(0.95)};
                font-size: 16px;
                font-weight: 400;
            }}
            QPushButton:hover {{
                background: {T.accent(0.28)};
                border-color: {T.accent(0.52)};
            }}
            QPushButton:pressed {{
                background: {T.accent(0.40)};
            }}
        """)

    def refresh_theme(self):
        self._apply_style()


class ChatInput(QLineEdit):
    """Input de texto del chat."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Escribe algo...")
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {T.text_primary()};
                font-size: 13px;
                selection-background-color: {T.accent(0.28)};
            }}
            QLineEdit::placeholder {{
                color: {T.text_hint()};
            }}
        """)

    def refresh_theme(self):
        self._apply_style()


class Toolbar(QWidget):
    """
    Barra inferior completa.

    Chips disponibles:
      · web       — toggle búsqueda web
      · extensiones — futuras integraciones
      · historial — ver historial de chats
      · nuevo     — nueva conversación

    Señales:
      message_sent(str)
      web_toggled(bool)
      history_requested()
      new_chat_requested()
    """

    message_sent      = pyqtSignal(str)
    web_toggled       = pyqtSignal(bool)
    history_requested = pyqtSignal()
    new_chat_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 14)
        layout.setSpacing(9)

        # --- Fila de input ---
        self._input  = ChatInput()
        self._send   = SendButton()

        input_row = QHBoxLayout()
        input_row.setSpacing(8)
        input_row.addWidget(self._input)
        input_row.addWidget(self._send)

        self._input_container = QWidget()
        self._input_container.setLayout(input_row)
        self._apply_input_style()

        # --- Fila de chips ---
        self._web_chip   = ToolChip("web",          checkable=True)
        self._ext_chip   = ToolChip("extensiones",  checkable=False)
        self._hist_chip  = ToolChip("historial",    checkable=False)
        self._new_chip   = ToolChip("+ nuevo",      checkable=False)

        self._web_chip.setChecked(True)

        self._model_label = QLabel("qwen2.5:7b")
        self._apply_model_label_style()

        chips_row = QHBoxLayout()
        chips_row.setSpacing(5)
        chips_row.setContentsMargins(0, 0, 0, 0)
        chips_row.addWidget(self._web_chip)
        chips_row.addWidget(self._ext_chip)
        chips_row.addWidget(self._hist_chip)
        chips_row.addWidget(self._new_chip)
        chips_row.addStretch()
        chips_row.addWidget(self._model_label)

        layout.addWidget(self._input_container)
        layout.addLayout(chips_row)

        self._apply_toolbar_style()

    def _apply_input_style(self):
        self._input_container.setStyleSheet(f"""
            QWidget {{
                background: {T.bg_input()};
                border: 1px solid {T.border_accent(0.16)};
                border-radius: 12px;
                padding: 2px 6px;
            }}
        """)

    def _apply_model_label_style(self):
        self._model_label.setStyleSheet(f"""
            color: {T.text_hint()};
            font-size: 10px;
        """)

    def _apply_toolbar_style(self):
        self.setStyleSheet(f"""
            Toolbar {{
                background: {T.bg_toolbar()};
                border-top: 1px solid {T.border_accent(0.08)};
            }}
        """)

    def _connect_signals(self):
        self._send.clicked.connect(self._send_message)
        self._input.returnPressed.connect(self._send_message)
        self._web_chip.toggled.connect(self._on_web_toggle)
        self._hist_chip.clicked.connect(self.history_requested)
        self._new_chip.clicked.connect(self.new_chat_requested)
        self._ext_chip.clicked.connect(lambda: None)  # placeholder

    def _send_message(self):
        text = self._input.text().strip()
        if text:
            self.message_sent.emit(text)
            self._input.clear()

    def _on_web_toggle(self, checked: bool):
        self.web_toggled.emit(checked)
        self._model_label.setText("qwen2.5:7b" if checked else "sin conexión")

    def refresh_theme(self):
        self._apply_input_style()
        self._apply_model_label_style()
        self._apply_toolbar_style()
        self._input.refresh_theme()
        self._send.refresh_theme()
        for chip in [self._web_chip, self._ext_chip, self._hist_chip, self._new_chip]:
            chip.refresh_theme()

    def set_model(self, model: str):
        self._model_label.setText(model)

    def set_enabled(self, enabled: bool):
        self._input.setEnabled(enabled)
        self._send.setEnabled(enabled)

"""
Área de mensajes de Kuro AI.
Scroll suave, mensajes apilados, typing indicator.
"""

from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot

from ui.bubble import MessageBubble, TypingBubble


class ChatWidget(QWidget):
    """Contenedor principal del historial de mensajes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._typing_widget = None
        self._build_ui()
        self._add_welcome()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Scroll area
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                width: 4px;
                background: transparent;
                margin: 4px 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(67, 210, 145, 0.20);
                border-radius: 2px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(67, 210, 145, 0.40);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Contenedor interno de mensajes
        self._msg_container = QWidget()
        self._msg_container.setStyleSheet("background: transparent;")
        self._msg_layout = QVBoxLayout(self._msg_container)
        self._msg_layout.setContentsMargins(16, 16, 16, 8)
        self._msg_layout.setSpacing(14)
        self._msg_layout.addStretch()  # Empuja mensajes hacia abajo

        self._scroll.setWidget(self._msg_container)
        layout.addWidget(self._scroll)

    def _add_welcome(self):
        """Mensaje de bienvenida inicial."""
        QTimer.singleShot(300, lambda: self.add_ai_message(
            "Hola. ¿En qué puedo ayudarte?"
        ))

    def add_user_message(self, text: str):
        """Agrega un mensaje del usuario y muestra typing indicator."""
        if not text.strip():
            return
        bubble = MessageBubble(text, role="user")
        self._insert_bubble(bubble)
        # Simular typing por ahora (luego se conecta a Ollama)
        QTimer.singleShot(200, self.show_typing)

    def add_ai_message(self, text: str, web_used: bool = False):
        """Agrega un mensaje de la AI."""
        self.hide_typing()
        bubble = MessageBubble(text, role="ai", web_used=web_used)
        self._insert_bubble(bubble)

    def show_typing(self):
        """Muestra el indicador de escritura."""
        if self._typing_widget:
            return
        self._typing_widget = TypingBubble()

        wrapper = QHBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.addWidget(self._typing_widget)
        wrapper.addStretch()

        container = QWidget()
        container.setLayout(wrapper)
        container.setObjectName("typing_container")

        # Insertar antes del stretch final
        count = self._msg_layout.count()
        self._msg_layout.insertWidget(count - 1, container)
        self._scroll_to_bottom()

    def hide_typing(self):
        """Oculta el indicador de escritura."""
        if not self._typing_widget:
            return
        for i in range(self._msg_layout.count()):
            item = self._msg_layout.itemAt(i)
            if item and item.widget() and item.widget().objectName() == "typing_container":
                w = item.widget()
                self._msg_layout.removeWidget(w)
                w.deleteLater()
                break
        self._typing_widget = None

    def _insert_bubble(self, bubble: MessageBubble):
        """Inserta una burbuja antes del stretch final."""
        count = self._msg_layout.count()
        self._msg_layout.insertWidget(count - 1, bubble)
        QTimer.singleShot(50, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        sb = self._scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    def clear(self):
        """Limpia todos los mensajes."""
        while self._msg_layout.count() > 1:
            item = self._msg_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

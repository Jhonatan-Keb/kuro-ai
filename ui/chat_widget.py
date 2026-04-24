"""
Área de mensajes de Kuro AI.
Scroll suave, burbujas apiladas, typing indicator.
"""

from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer

from ui.bubble import MessageBubble, TypingBubble
import ui.theme as T


class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._typing_widget = None
        self._bubbles: list[MessageBubble] = []
        self._build_ui()
        QTimer.singleShot(350, lambda: self.add_ai_message("Hola. ¿En qué puedo ayudarte?"))

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._apply_scroll_style()

        self._msg_container = QWidget()
        self._msg_container.setStyleSheet("background: transparent;")
        self._msg_layout = QVBoxLayout(self._msg_container)
        self._msg_layout.setContentsMargins(16, 16, 16, 8)
        self._msg_layout.setSpacing(14)
        self._msg_layout.addStretch()

        self._scroll.setWidget(self._msg_container)
        layout.addWidget(self._scroll)

    def _apply_scroll_style(self):
        self._scroll.setStyleSheet(f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{
                width: 4px; background: transparent; margin: 4px 2px;
            }}
            QScrollBar::handle:vertical {{
                background: {T.scrollbar_handle()};
                border-radius: 2px; min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {T.accent(0.40)};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

    def add_user_message(self, text: str):
        if not text.strip():
            return
        bubble = MessageBubble(text, role="user")
        self._bubbles.append(bubble)
        self._insert_widget(bubble)
        QTimer.singleShot(180, self.show_typing)

    def add_ai_message(self, text: str, web_used: bool = False):
        self.hide_typing()
        bubble = MessageBubble(text, role="ai", web_used=web_used)
        self._bubbles.append(bubble)
        self._insert_widget(bubble)

    def show_typing(self):
        if self._typing_widget:
            return
        self._typing_widget = TypingBubble()
        wrapper = QWidget()
        wrapper.setObjectName("typing_container")
        wrapper.setStyleSheet("background: transparent;")
        row = QHBoxLayout(wrapper)
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(self._typing_widget)
        row.addStretch()
        count = self._msg_layout.count()
        self._msg_layout.insertWidget(count - 1, wrapper)
        self._scroll_to_bottom()

    def hide_typing(self):
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

    def _insert_widget(self, widget: QWidget):
        count = self._msg_layout.count()
        self._msg_layout.insertWidget(count - 1, widget)
        QTimer.singleShot(40, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        sb = self._scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    def refresh_theme(self):
        self._apply_scroll_style()
        self._msg_container.setStyleSheet("background: transparent;")
        for bubble in self._bubbles:
            bubble.refresh_theme()
        if self._typing_widget:
            self._typing_widget.refresh_theme()

    def clear(self):
        self._bubbles.clear()
        while self._msg_layout.count() > 1:
            item = self._msg_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

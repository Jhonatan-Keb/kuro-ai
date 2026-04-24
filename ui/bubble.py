"""
Burbujas de chat individuales para Kuro AI.
Colores adaptativos via ui.theme.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
import ui.theme as T


class WebBadge(QLabel):
    def __init__(self, parent=None):
        super().__init__("  web", parent)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QLabel {{
                color: {T.accent(0.80)};
                background: {T.accent(0.07)};
                border: 1px solid {T.accent(0.16)};
                border-radius: 4px;
                padding: 2px 7px;
                font-size: 9px;
            }}
        """)

    def refresh_theme(self):
        self._apply_style()


class TypingBubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 11, 14, 11)
        layout.setSpacing(5)
        self._dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {T.accent(0.55)}; font-size: 7px;")
            layout.addWidget(dot)
            self._dots.append(dot)
        layout.addStretch()
        self.setMaximumWidth(72)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            TypingBubble {{
                background: {T.bubble_ai_bg()};
                border: 1px solid {T.bubble_ai_border()};
                border-radius: 14px;
                border-bottom-left-radius: 4px;
            }}
        """)

    def refresh_theme(self):
        self._apply_style()
        for dot in self._dots:
            dot.setStyleSheet(f"color: {T.accent(0.55)}; font-size: 7px;")


class MessageBubble(QWidget):
    """
    Burbuja completa: label de autor + (badge web) + texto.
    role: 'user' | 'ai'
    """

    def __init__(self, text: str, role: str = "ai", web_used: bool = False, parent=None):
        super().__init__(parent)
        self.role = role
        self._web_badge = None

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        col = QVBoxLayout()
        col.setSpacing(4)
        col.setContentsMargins(0, 0, 0, 0)

        # Autor
        self._author = QLabel("Kuro" if role == "ai" else "Tú")
        col.addWidget(self._author)

        # Badge web
        if role == "ai" and web_used:
            self._web_badge = WebBadge()
            col.addWidget(self._web_badge)

        # Texto
        self._bubble = QLabel(text)
        self._bubble.setWordWrap(True)
        self._bubble.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self._bubble.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Minimum
        )
        col.addWidget(self._bubble)

        if role == "user":
            outer.addStretch()
        outer.addLayout(col)
        if role == "ai":
            outer.addStretch()

        self._apply_style()

    def _apply_style(self):
        if self.role == "ai":
            self._author.setStyleSheet(f"""
                color: {T.accent(0.55)};
                font-size: 9px;
                font-weight: 500;
                letter-spacing: 1.5px;
                text-transform: uppercase;
            """)
            self._bubble.setStyleSheet(f"""
                QLabel {{
                    background: {T.bubble_ai_bg()};
                    border: 1px solid {T.bubble_ai_border()};
                    border-radius: 14px;
                    border-bottom-left-radius: 4px;
                    color: {T.text_primary()};
                    font-size: 13px;
                    padding: 10px 14px;
                }}
            """)
        else:
            self._author.setStyleSheet(f"""
                color: {T.purple(0.55)};
                font-size: 9px;
                font-weight: 500;
                letter-spacing: 1.5px;
                text-transform: uppercase;
            """)
            self._bubble.setStyleSheet(f"""
                QLabel {{
                    background: {T.bubble_user_bg()};
                    border: 1px solid {T.bubble_user_border()};
                    border-radius: 14px;
                    border-bottom-right-radius: 4px;
                    color: {T.text_primary()};
                    font-size: 13px;
                    padding: 10px 14px;
                }}
            """)
        if self._web_badge:
            self._web_badge.refresh_theme()

    def refresh_theme(self):
        self._apply_style()

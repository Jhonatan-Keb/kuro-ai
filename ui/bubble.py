"""
Burbujas de chat individuales para Kuro AI.
Estilo glassmorphism oscuro: verde Dendro para AI, púrpura para usuario.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor


class WebBadge(QLabel):
    """Indicador pequeño de que se usó búsqueda web."""

    def __init__(self, parent=None):
        super().__init__("  buscando en web...", parent)
        self.setStyleSheet("""
            QLabel {
                color: rgba(67, 210, 145, 0.75);
                background: rgba(67, 210, 145, 0.07);
                border: 1px solid rgba(67, 210, 145, 0.15);
                border-radius: 5px;
                padding: 2px 7px;
                font-size: 10px;
                font-family: 'JetBrainsMono Nerd Font Mono', monospace;
            }
        """)


class TypingBubble(QWidget):
    """Tres puntitos animados mientras la AI genera respuesta."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(5)

        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet(f"""
                color: rgba(67, 210, 145, 0.6);
                font-size: 8px;
            """)
            dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(dot)
            self._animate_dot(dot, delay=i * 200)

        layout.addStretch()
        self.setMaximumWidth(80)
        self.setStyleSheet("""
            TypingBubble {
                background: rgba(67, 210, 145, 0.07);
                border: 1px solid rgba(67, 210, 145, 0.14);
                border-radius: 14px;
                border-bottom-left-radius: 4px;
            }
        """)

    def _animate_dot(self, dot: QLabel, delay: int):
        anim = QPropertyAnimation(dot, b"maximumHeight")
        anim.setDuration(600)
        anim.setStartValue(20)
        anim.setEndValue(8)
        anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        anim.setLoopCount(-1)
        anim.start()
        self._anim = anim


class MessageBubble(QWidget):
    """
    Burbuja de mensaje completa con label de autor y contenido.
    role: 'user' | 'ai'
    """

    def __init__(self, text: str, role: str = "ai", web_used: bool = False, parent=None):
        super().__init__(parent)
        self.role = role

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        col = QVBoxLayout()
        col.setSpacing(4)

        # Label de autor
        author = QLabel("Kuro" if role == "ai" else "Tú")
        if role == "ai":
            author.setStyleSheet("""
                color: rgba(67, 210, 145, 0.55);
                font-size: 9px;
                font-weight: 500;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                font-family: 'JetBrainsMono Nerd Font Mono', monospace;
            """)
        else:
            author.setStyleSheet("""
                color: rgba(138, 90, 220, 0.55);
                font-size: 9px;
                font-weight: 500;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                font-family: 'JetBrainsMono Nerd Font Mono', monospace;
            """)
        col.addWidget(author)

        # Badge web (solo para AI cuando usó búsqueda)
        if role == "ai" and web_used:
            col.addWidget(WebBadge())

        # Burbuja de texto
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        bubble.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        if role == "ai":
            bubble.setStyleSheet("""
                QLabel {
                    background: rgba(67, 210, 145, 0.07);
                    border: 1px solid rgba(67, 210, 145, 0.15);
                    border-radius: 14px;
                    border-bottom-left-radius: 4px;
                    color: rgba(255, 255, 255, 0.88);
                    font-size: 13px;
                    line-height: 1.55;
                    padding: 10px 14px;
                    font-family: 'JetBrainsMono Nerd Font Mono', monospace;
                }
            """)
        else:
            bubble.setStyleSheet("""
                QLabel {
                    background: rgba(138, 90, 220, 0.13);
                    border: 1px solid rgba(138, 90, 220, 0.22);
                    border-radius: 14px;
                    border-bottom-right-radius: 4px;
                    color: rgba(255, 255, 255, 0.88);
                    font-size: 13px;
                    line-height: 1.55;
                    padding: 10px 14px;
                    font-family: 'JetBrainsMono Nerd Font Mono', monospace;
                }
            """)

        col.addWidget(bubble)

        if role == "user":
            outer.addStretch()
        outer.addLayout(col)
        if role == "ai":
            outer.addStretch()

        self.setMaximumWidth(340)
        if role == "user":
            self.setContentsMargins(60, 0, 0, 0)
        else:
            self.setContentsMargins(0, 0, 60, 0)

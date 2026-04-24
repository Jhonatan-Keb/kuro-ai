"""
Ventana principal de Kuro AI.
Frameless, draggable, always-on-top, glassmorphism oscuro Dendro.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QLinearGradient

from ui.chat_widget import ChatWidget
from ui.toolbar import Toolbar


ACCENT       = "#43d291"
ACCENT_DIM   = "rgba(67, 210, 145, 0.18)"
BG_DARK      = "#0a0d12"
BG_PANEL     = "rgba(255, 255, 255, 0.04)"
BORDER_COLOR = "rgba(67, 210, 145, 0.18)"


class TitleBar(QWidget):
    """Barra de título custom con traffic lights y título."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)

        # Traffic lights
        dots_layout = QHBoxLayout()
        dots_layout.setSpacing(7)
        for color, tip in [("#ff5f57", "Cerrar"), ("#febc2e", "Minimizar"), ("#28c840", "Maximizar")]:
            btn = QPushButton()
            btn.setFixedSize(11, 11)
            btn.setToolTip(tip)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    border-radius: 5px;
                    border: none;
                }}
                QPushButton:hover {{ opacity: 0.7; }}
            """)
            dots_layout.addWidget(btn)
        layout.addLayout(dots_layout)
        layout.addSpacing(12)

        # Título
        title = QLabel("Kuro AI")
        title.setStyleSheet(f"""
            color: {ACCENT};
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-family: 'JetBrainsMono Nerd Font Mono', monospace;
        """)
        layout.addWidget(title)
        layout.addStretch()

        # Status pill
        self.status_pill = StatusPill()
        layout.addWidget(self.status_pill)

        self.setStyleSheet(f"""
            TitleBar {{
                background: rgba(67, 210, 145, 0.04);
                border-bottom: 1px solid rgba(67, 210, 145, 0.10);
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


class StatusPill(QWidget):
    """Indicador de estado online/offline con punto pulsante."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 10, 3)
        layout.setSpacing(5)

        self._dot = QLabel()
        self._dot.setFixedSize(7, 7)
        self._dot.setStyleSheet("""
            QLabel {
                background: #43d291;
                border-radius: 3px;
            }
        """)

        self._label = QLabel("local · qwen2.5")
        self._label.setStyleSheet("""
            color: rgba(255,255,255,0.35);
            font-size: 10px;
            font-family: 'JetBrainsMono Nerd Font Mono', monospace;
        """)

        layout.addWidget(self._dot)
        layout.addWidget(self._label)

        self.setStyleSheet("""
            StatusPill {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 10px;
            }
        """)

    def set_online(self, online: bool, model: str = "qwen2.5"):
        if online:
            self._dot.setStyleSheet("QLabel { background: #43d291; border-radius: 3px; }")
            self._label.setText(f"local · {model}")
        else:
            self._dot.setStyleSheet("QLabel { background: #888780; border-radius: 3px; }")
            self._label.setText("offline · local")


class KuroWindow(QMainWindow):
    """
    Ventana principal frameless de Kuro AI.
    Glassmorphism oscuro, siempre encima, draggable.
    """

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._build_ui()
        self._apply_styles()

    def _setup_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(400, 620)

        # Centrar en pantalla
        screen = self.screen().availableGeometry()
        self.move(
            screen.width() - self.width() - 40,
            (screen.height() - self.height()) // 2
        )

    def _build_ui(self):
        # Contenedor raíz con borde redondeado
        self._root = QWidget()
        self._root.setObjectName("KuroRoot")
        self.setCentralWidget(self._root)

        layout = QVBoxLayout(self._root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # TitleBar
        self.titlebar = TitleBar(self)
        self.titlebar.findChildren(QPushButton)[0].clicked.connect(self.close)
        self.titlebar.findChildren(QPushButton)[1].clicked.connect(self.showMinimized)
        layout.addWidget(self.titlebar)

        # Área de chat
        self.chat = ChatWidget()
        layout.addWidget(self.chat, stretch=1)

        # Toolbar inferior
        self.toolbar = Toolbar()
        self.toolbar.web_toggled.connect(self._on_web_toggle)
        self.toolbar.message_sent.connect(self.chat.add_user_message)
        layout.addWidget(self.toolbar)

        # Sombra exterior
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 180))
        self._root.setGraphicsEffect(shadow)

    def _apply_styles(self):
        self._root.setStyleSheet(f"""
            QWidget#KuroRoot {{
                background: rgba(10, 13, 18, 0.92);
                border: 1px solid rgba(67, 210, 145, 0.18);
                border-radius: 18px;
            }}
        """)

    def _on_web_toggle(self, enabled: bool):
        self.titlebar.status_pill.set_online(enabled)

    def toggle_visibility(self):
        """Llamado desde el hotkey F24."""
        if self.isVisible():
            self._animate_hide()
        else:
            self._animate_show()

    def _animate_show(self):
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(180)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._anim = anim

    def _animate_hide(self):
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(150)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.InCubic)
        anim.finished.connect(self.hide)
        anim.start()
        self._anim = anim

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._animate_hide()
        super().keyPressEvent(event)

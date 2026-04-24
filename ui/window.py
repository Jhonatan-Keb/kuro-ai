"""
Ventana principal de Kuro AI.
Frameless, draggable, always-on-top, glassmorphism oscuro Dendro.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGraphicsDropShadowEffect, QStyle
)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QSize
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QLinearGradient, QIcon

from ui.chat_widget import ChatWidget
from ui.toolbar import Toolbar


ACCENT       = "#43d291"
ACCENT_DIM   = "rgba(67, 210, 145, 0.18)"
BG_DARK      = "#0a0d12"
BG_PANEL     = "rgba(255, 255, 255, 0.04)"
BORDER_COLOR = "rgba(67, 210, 145, 0.18)"


class WindowControlButton(QPushButton):
    """
    Botón de control de ventana (cerrar/minimizar) que usa
    los iconos nativos del estilo Qt activo — se adapta al tema KDE.
    """

    def __init__(self, pixel_metric, tooltip: str, parent=None):
        super().__init__(parent)
        self._pixel_metric = pixel_metric
        self.setToolTip(tooltip)
        self.setFixedSize(28, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 6px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.12);
                border-color: rgba(255,255,255,0.18);
            }
            QPushButton:pressed {
                background: rgba(255,255,255,0.20);
            }
        """)

    def _get_system_icon(self, style_pixel) -> QIcon:
        """Obtiene el icono del estilo del sistema activo."""
        style = self.style()
        if style:
            return style.standardIcon(style_pixel)
        return QIcon()

    def paintEvent(self, event):
        super().paintEvent(event)
        # Dibujar el icono del sistema encima del botón base
        icon_map = {
            "close":    QStyle.StandardPixmap.SP_TitleBarCloseButton,
            "minimize": QStyle.StandardPixmap.SP_TitleBarMinButton,
        }
        # Guardamos el tipo en el tooltip para saber cuál dibujar
        key = "close" if "Cerrar" in self.toolTip() else "minimize"
        icon = self.style().standardIcon(icon_map[key])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        icon.paint(painter, 4, 4, 20, 20)
        painter.end()


class TitleBar(QWidget):
    """Barra de título custom con botones nativos del sistema y título."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(0)

        # Botones de control usando iconos del sistema
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(6)

        self._btn_close = WindowControlButton(
            QStyle.StandardPixmap.SP_TitleBarCloseButton, "Cerrar"
        )
        self._btn_minimize = WindowControlButton(
            QStyle.StandardPixmap.SP_TitleBarMinButton, "Minimizar"
        )

        controls_layout.addWidget(self._btn_close)
        controls_layout.addWidget(self._btn_minimize)
        layout.addLayout(controls_layout)
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

        # TitleBar — botones conectados directamente por referencia
        self.titlebar = TitleBar(self)
        self.titlebar._btn_close.clicked.connect(self.close)
        self.titlebar._btn_minimize.clicked.connect(self.showMinimized)
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

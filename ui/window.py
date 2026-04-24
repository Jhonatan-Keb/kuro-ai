"""
Ventana principal de Kuro AI.
Frameless, draggable, always-on-top, glassmorphism Dendro.
Detecta posición de botones del sistema (Windows-style derecha / otros izquierda).
Se adapta automáticamente a tema claro/oscuro del sistema.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGraphicsDropShadowEffect, QStyle, QApplication
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor, QPainter, QFont, QFontDatabase, QPalette

from ui.chat_widget import ChatWidget
from ui.toolbar import Toolbar
import ui.theme as T


def system_font() -> QFont:
    """Fuente del sistema, no hardcodeada."""
    return QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)


def buttons_on_right() -> bool:
    """
    Detecta si el sistema pone los botones de ventana a la derecha.
    KDE/Windows → derecha. macOS → izquierda.
    Lee el hint del estilo Qt activo.
    """
    style = QApplication.style()
    if style is None:
        return True
    name = style.objectName().lower()
    # macOS es el único que los pone a la izquierda de forma nativa
    return "mac" not in name and "aqua" not in name


class WindowControlButton(QPushButton):
    """
    Botón de control de ventana con icono nativo del sistema.
    Se repinta automáticamente cuando cambia el tema.
    """

    ICONS = {
        "close":    QStyle.StandardPixmap.SP_TitleBarCloseButton,
        "minimize": QStyle.StandardPixmap.SP_TitleBarMinButton,
    }

    def __init__(self, kind: str, tooltip: str, parent=None):
        super().__init__(parent)
        self._kind = kind
        self.setToolTip(tooltip)
        self.setFixedSize(26, 26)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: {T.win_btn_bg()};
                border: 1px solid {T.win_btn_border()};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background: {T.win_btn_hover()};
            }}
            QPushButton:pressed {{
                background: {T.accent(0.22)};
            }}
        """)

    def refresh_theme(self):
        self._apply_style()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        icon = self.style().standardIcon(self.ICONS[self._kind])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        icon.paint(painter, 3, 3, 20, 20)
        painter.end()


class StatusPill(QWidget):
    """Indicador de estado online/offline. Respeta tema claro/oscuro."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 10, 3)
        layout.setSpacing(5)

        self._dot = QLabel()
        self._dot.setFixedSize(7, 7)

        self._label = QLabel("local · qwen2.5")
        self._online = True
        self._model = "qwen2.5"

        layout.addWidget(self._dot)
        layout.addWidget(self._label)
        self._apply_style()

    def _apply_style(self):
        dot_color = T.ACCENT if self._online else "#888780"
        self._dot.setStyleSheet(f"QLabel {{ background: {dot_color}; border-radius: 3px; }}")
        self._label.setStyleSheet(f"""
            color: {T.text_secondary()};
            font-size: 10px;
        """)
        self.setStyleSheet(f"""
            StatusPill {{
                background: {T.bg_input()};
                border: 1px solid {T.border_accent(0.12)};
                border-radius: 10px;
            }}
        """)

    def set_online(self, online: bool, model: str = None):
        self._online = online
        if model:
            self._model = model
        self._label.setText(f"local · {self._model}" if online else "offline · local")
        self._apply_style()

    def refresh_theme(self):
        self._apply_style()


class TitleBar(QWidget):
    """
    Barra de título. Posición de botones según el sistema:
    - KDE/Windows/GNOME → botones a la DERECHA (título a la izquierda)
    - macOS/Aqua         → botones a la izquierda
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(46)
        self._drag_pos = None
        self._right_side = buttons_on_right()
        self._build_layout()

    def _build_layout(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(8)

        # Título
        self._title = QLabel("Kuro AI")
        self._title.setStyleSheet(f"""
            color: {T.accent()};
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
        """)

        # Botones de control
        self._btn_close    = WindowControlButton("close",    "Cerrar")
        self._btn_minimize = WindowControlButton("minimize", "Minimizar")

        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(5)
        ctrl_layout.setContentsMargins(0, 0, 0, 0)
        ctrl_layout.addWidget(self._btn_close)
        ctrl_layout.addWidget(self._btn_minimize)

        # Status pill (siempre a la izquierda si botones van a la derecha)
        self.status_pill = StatusPill()

        if self._right_side:
            # Windows/KDE: [título]  [...]  [status] [─] [✕]
            layout.addWidget(self._title)
            layout.addStretch()
            layout.addWidget(self.status_pill)
            layout.addSpacing(6)
            layout.addLayout(ctrl_layout)
        else:
            # macOS: [✕][─]  [título]  [...] [status]
            layout.addLayout(ctrl_layout)
            layout.addSpacing(8)
            layout.addWidget(self._title)
            layout.addStretch()
            layout.addWidget(self.status_pill)

        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            TitleBar {{
                background: {T.bg_titlebar()};
                border-bottom: 1px solid {T.border_accent(0.10)};
            }}
        """)

    def refresh_theme(self):
        self._apply_style()
        self._title.setStyleSheet(f"""
            color: {T.accent()};
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
        """)
        self._btn_close.refresh_theme()
        self._btn_minimize.refresh_theme()
        self.status_pill.refresh_theme()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() -
                self.window().frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(
                event.globalPosition().toPoint() - self._drag_pos
            )

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


class KuroWindow(QMainWindow):
    """
    Ventana principal frameless de Kuro AI.
    Glassmorphism, siempre encima, draggable, tema adaptativo.
    """

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._build_ui()
        self._apply_styles()
        self._setup_theme_watcher()

    def _setup_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Fuente del sistema (no hardcodeada)
        app_font = system_font()
        app_font.setPointSize(10)
        QApplication.setFont(app_font)

        self.resize(400, 620)
        screen = self.screen().availableGeometry()
        self.move(
            screen.width() - self.width() - 40,
            (screen.height() - self.height()) // 2
        )

    def _build_ui(self):
        self._root = QWidget()
        self._root.setObjectName("KuroRoot")
        self.setCentralWidget(self._root)

        layout = QVBoxLayout(self._root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.titlebar = TitleBar(self)
        self.titlebar._btn_close.clicked.connect(self.close)
        self.titlebar._btn_minimize.clicked.connect(self.showMinimized)
        layout.addWidget(self.titlebar)

        self.chat = ChatWidget()
        layout.addWidget(self.chat, stretch=1)

        self.toolbar = Toolbar()
        self.toolbar.web_toggled.connect(self._on_web_toggle)
        self.toolbar.message_sent.connect(self.chat.add_user_message)
        layout.addWidget(self.toolbar)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(55)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))
        self._root.setGraphicsEffect(shadow)

    def _apply_styles(self):
        self._root.setStyleSheet(f"""
            QWidget#KuroRoot {{
                background: {T.bg_window()};
                border: 1px solid {T.border_accent(0.18)};
                border-radius: 16px;
            }}
        """)

    def _setup_theme_watcher(self):
        """Detecta cambios de tema del sistema cada 2s y refresca si cambió."""
        self._last_dark = T.is_dark()
        self._theme_timer = QTimer(self)
        self._theme_timer.setInterval(2000)
        self._theme_timer.timeout.connect(self._check_theme_change)
        self._theme_timer.start()

    def _check_theme_change(self):
        now_dark = T.is_dark()
        if now_dark != self._last_dark:
            self._last_dark = now_dark
            self._refresh_all_themes()

    def _refresh_all_themes(self):
        self._apply_styles()
        self.titlebar.refresh_theme()
        self.toolbar.refresh_theme()
        self.chat.refresh_theme()

    def _on_web_toggle(self, enabled: bool):
        self.titlebar.status_pill.set_online(enabled)

    def toggle_visibility(self):
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

"""
Sistema de temas de Kuro AI.
Detecta si el sistema usa tema claro u oscuro via QPalette,
y expone colores adaptados manteniendo la estética Dendro/glassmorphism.
Se actualiza automáticamente cuando el sistema cambia de tema.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor


ACCENT = "#43d291"
ACCENT_RGB = (67, 210, 145)
PURPLE_RGB = (138, 90, 220)


def is_dark() -> bool:
    """True si el tema del sistema es oscuro."""
    palette = QApplication.instance().palette()
    bg = palette.color(QPalette.ColorRole.Window)
    # Si el fondo del sistema es más oscuro que gris medio → dark
    return bg.lightness() < 128


def accent(alpha: float = 1.0) -> str:
    r, g, b = ACCENT_RGB
    if alpha >= 1.0:
        return f"#{r:02x}{g:02x}{b:02x}"
    return f"rgba({r},{g},{b},{alpha})"


def purple(alpha: float = 1.0) -> str:
    r, g, b = PURPLE_RGB
    return f"rgba({r},{g},{b},{alpha})"


def bg_window() -> str:
    """Fondo principal de la ventana."""
    return "rgba(10,13,18,0.93)" if is_dark() else "rgba(240,244,248,0.93)"


def bg_titlebar() -> str:
    return accent(0.04) if is_dark() else accent(0.06)


def bg_input() -> str:
    return "rgba(255,255,255,0.04)" if is_dark() else "rgba(255,255,255,0.70)"


def bg_toolbar() -> str:
    return "rgba(0,0,0,0.18)" if is_dark() else "rgba(0,0,0,0.04)"


def text_primary() -> str:
    return "rgba(255,255,255,0.88)" if is_dark() else "rgba(10,13,18,0.90)"


def text_secondary() -> str:
    return "rgba(255,255,255,0.38)" if is_dark() else "rgba(10,13,18,0.45)"


def text_hint() -> str:
    return "rgba(255,255,255,0.22)" if is_dark() else "rgba(10,13,18,0.28)"


def border_accent(alpha: float = 0.18) -> str:
    r, g, b = ACCENT_RGB
    return f"rgba({r},{g},{b},{alpha})"


def bubble_ai_bg() -> str:
    return accent(0.07) if is_dark() else accent(0.10)


def bubble_ai_border() -> str:
    return accent(0.15) if is_dark() else accent(0.30)


def bubble_user_bg() -> str:
    return purple(0.13) if is_dark() else purple(0.10)


def bubble_user_border() -> str:
    return purple(0.22) if is_dark() else purple(0.35)


def chip_active_bg() -> str:
    return accent(0.09) if is_dark() else accent(0.14)


def chip_active_border() -> str:
    return accent(0.32) if is_dark() else accent(0.50)


def chip_inactive_border() -> str:
    return "rgba(255,255,255,0.07)" if is_dark() else "rgba(0,0,0,0.12)"


def chip_inactive_text() -> str:
    return "rgba(255,255,255,0.30)" if is_dark() else "rgba(0,0,0,0.40)"


def scrollbar_handle() -> str:
    return accent(0.20) if is_dark() else accent(0.35)


def win_btn_bg() -> str:
    return "rgba(255,255,255,0.05)" if is_dark() else "rgba(0,0,0,0.06)"


def win_btn_border() -> str:
    return "rgba(255,255,255,0.09)" if is_dark() else "rgba(0,0,0,0.12)"


def win_btn_hover() -> str:
    return "rgba(255,255,255,0.13)" if is_dark() else "rgba(0,0,0,0.10)"

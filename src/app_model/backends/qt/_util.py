from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import QObject
from qtpy.QtGui import QIcon, QPalette
from qtpy.QtWidgets import QApplication

if TYPE_CHECKING:
    from typing import Literal

    from app_model.types import Icon


def luma(r: float, g: float, b: float) -> float:
    """Calculate the relative luminance of a color."""
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def background_luma(qobj: QObject | None = None) -> float:
    """Return background luminance of the first top level widget or QApp."""
    # using hasattr here because it will only work with a QWidget, but some of the
    # things calling this function could conceivably only be a QObject
    if hasattr(qobj, "palette"):
        palette: QPalette = qobj.palette()  # type: ignore
    elif wdgts := QApplication.topLevelWidgets():
        palette = wdgts[0].palette()
    else:  # pragma: no cover
        palette = QApplication.palette()
    window_bgrd = palette.color(QPalette.ColorRole.Window)
    return luma(window_bgrd.redF(), window_bgrd.greenF(), window_bgrd.blueF())


LIGHT_COLOR = "#BCB4B4"
DARK_COLOR = "#6B6565"


def to_qicon(
    icon: Icon,
    theme: Literal["dark", "light", None] = None,
    color: str | None = None,
    parent: QObject | None = None,
) -> QIcon:
    """Create QIcon from Icon."""
    from superqt import QIconifyIcon, fonticon

    if theme is None:
        theme = "dark" if background_luma(parent) < 0.5 else "light"
    if color is None:
        # use DARK_COLOR icon for light themes and vice versa
        color = (
            (icon.color_dark or LIGHT_COLOR)
            if theme == "dark"
            else (icon.color_light or DARK_COLOR)
        )

    if icn := getattr(icon, theme, ""):
        if ":" in icn:
            return QIconifyIcon(icn, color=color)
        else:
            return fonticon.icon(icn, color=color)
    return QIcon()  # pragma: no cover

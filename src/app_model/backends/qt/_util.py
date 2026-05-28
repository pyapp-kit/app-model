from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from qtpy.QtCore import QEvent, QObject, QTimer, QUrl
from qtpy.QtGui import QIcon, QPalette
from qtpy.QtWidgets import QApplication

if TYPE_CHECKING:
    from typing import Literal

    from app_model import Application
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


def guess_theme_mode(
    theme: Literal["dark", "light", None] = None,
    parent: QObject | None = None,
) -> Literal["dark", "light"]:
    return theme or ("dark" if background_luma(parent) < 0.5 else "light")


def pick_icon_color(
    icon: Icon,
    theme: Literal["dark", "light"],
    default_colors: tuple[str, str],
) -> str:
    return (
        (icon.color_dark or default_colors[0])
        if theme == "dark"
        else (icon.color_light or default_colors[1])
    )


def to_qicon(
    icon: Icon,
    theme: Literal["dark", "light"],
    color: str | None = None,
) -> QIcon:
    """Create QIcon from Icon."""
    from superqt import QIconifyIcon, fonticon

    if icn := getattr(icon, theme, ""):
        if icn.startswith("file://"):
            return QIcon(QUrl(icn).toLocalFile())
        elif ":" in icn:
            return QIconifyIcon(icn, color=color)
        else:
            return fonticon.icon(icn, color=color)
    return QIcon()  # pragma: no cover


class ThemeEventFilter(QObject):
    """Event filter triggering theme change on palette modification."""

    def __init__(self, app: Application) -> None:
        super().__init__()
        self._app = app
        self._app._theme_event_filter = self  # type: ignore[attr-defined]

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if (
            a0 is QApplication.instance()
            and a1 is not None
            and a1.type()
            in (
                QEvent.Type.ApplicationPaletteChange,
                QEvent.Type.PaletteChange,
                QEvent.Type.StyleChange,
            )
        ):
            # delay firing slightly, so the colors can properly propagate via the
            # palette change (otherwise our icons will detect the *old* color)
            QTimer.singleShot(1, partial(self._app.theme_changed, self._app.theme_mode))
        return False

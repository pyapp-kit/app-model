from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import QUrl
from qtpy.QtGui import QIcon

if TYPE_CHECKING:
    from typing import Literal

    from app_model.types import Icon


def to_qicon(icon: Icon, theme: Literal["dark", "light"] = "dark") -> QIcon:
    """Create QIcon from Icon."""
    from superqt import QIconifyIcon, fonticon

    color = 'white' if theme == 'dark' else 'black'
    if icn := getattr(icon, theme, ""):
        if icn.startswith("file://"):
            return QIcon(QUrl(icn).toLocalFile())
        elif ":" in icn:
            return QIconifyIcon(icn, color=color)
        else:
            return fonticon.icon(icn, color=color)
    return QIcon()  # pragma: no cover

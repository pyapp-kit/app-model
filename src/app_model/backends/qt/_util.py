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

    if icn := getattr(icon, theme, ""):
        if icn.startswith("file://"):
            return QIcon(QUrl(icn).toLocalFile())
        elif ":" in icn:
            return QIconifyIcon(icn)
        else:
            return fonticon.icon(icn)
    return QIcon()  # pragma: no cover

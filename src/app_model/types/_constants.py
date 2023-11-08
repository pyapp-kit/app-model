import os
import sys
from enum import Enum


class OperatingSystem(Enum):
    """Operating system enum."""

    UNKNOWN = 0
    WINDOWS = 1
    MACOS = 2
    LINUX = 3

    @staticmethod
    def current() -> "OperatingSystem":
        """Return the current operating system as enum."""
        return _CURRENT

    @property
    def is_windows(self) -> bool:
        """Returns True if the current operating system is Windows."""
        return _CURRENT == OperatingSystem.WINDOWS

    @property
    def is_linux(self) -> bool:
        """Returns True if the current operating system is Linux."""
        return _CURRENT == OperatingSystem.LINUX

    @property
    def is_mac(self) -> bool:
        """Returns True if the current operating system is MacOS."""
        return _CURRENT == OperatingSystem.MACOS


_CURRENT = OperatingSystem.UNKNOWN
if os.name == "nt":
    _CURRENT = OperatingSystem.WINDOWS
if sys.platform.startswith("linux"):
    _CURRENT = OperatingSystem.LINUX
elif sys.platform == "darwin":
    _CURRENT = OperatingSystem.MACOS

"""Generic application schema implemented in python."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("app-model")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "uninstalled"
__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"

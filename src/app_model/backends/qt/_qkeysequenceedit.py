from typing import TYPE_CHECKING, Optional

from qtpy.QtWidgets import QKeySequenceEdit

from ._qkeymap import qkeysequence2modelkeybinding

if TYPE_CHECKING:
    from app_model.types import KeyBinding


class QModelKeyBindingEdit(QKeySequenceEdit):
    """Editor for a KeyBinding instance.

    This is a QKeySequenceEdit with a method that converts the current
    keySequence to an app_model KeyBinding instance.
    """

    def keyBinding(self) -> Optional["KeyBinding"]:
        """Return app_model KeyBinding instance for the current keySequence."""
        if self.keySequence().isEmpty():
            return None
        return qkeysequence2modelkeybinding(self.keySequence())

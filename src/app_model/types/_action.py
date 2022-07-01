from typing import Callable, Generic, List, Optional, TypeVar

from pydantic import Field
from typing_extensions import ParamSpec

from ._command import CommandRule
from ._keybinding import KeybindingRule
from ._menu import MenuRule

P = ParamSpec("P")
R = TypeVar("R")


class Action(CommandRule, Generic[P, R]):
    """Callable object along with specific context, menu, keybindings logic.

    This is the "complete" representation of a command.  Including a pointer to the
    actual callable object, as well as any additional menu and keybinding rules.
    Most commands and menu items will be represented by Actions, and registered using
    `register_action`.
    """

    # TODO: this could also be a string
    callback: Callable[P, R] = Field(
        ...,
        description="A function to call when the associated command id is executed.",
    )
    menus: Optional[List[MenuRule]] = Field(
        None,
        description="(Optional) Menus to which this action should be added.",
    )
    keybindings: Optional[List[KeybindingRule]] = Field(
        None,
        description="(Optional) Default keybinding(s) that will trigger this command.",
    )
    add_to_command_palette: bool = Field(
        True,
        description="Whether to add this command to the global Command Palette "
        "during registration.",
    )

    def run(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Run the command."""
        return self.callback(*args, **kwargs)

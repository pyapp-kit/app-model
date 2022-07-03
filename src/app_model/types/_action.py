from typing import Callable, Generic, List, Optional, TypeVar, Union

from pydantic import Field, validator
from typing_extensions import ParamSpec

from ._command_rule import CommandRule
from ._keybinding_rule import KeyBindingRule
from ._menu import MenuRule
from ._utils import _validate_python_name

P = ParamSpec("P")
R = TypeVar("R")


class Action(CommandRule, Generic[P, R]):
    """Callable object along with specific context, menu, keybindings logic.

    This is the "complete" representation of a command.  Including a pointer to the
    actual callable object, as well as any additional menu and keybinding rules.
    Most commands and menu items will be represented by Actions, and registered using
    `register_action`.
    """

    callback: Union[Callable[P, R], str] = Field(
        ...,
        description="A function to call when the associated command id is executed. "
        "If a string is provided, it must be a fully qualified name to a callable "
        "python object. This usually takes the form of "
        "`{obj.__module__}:{obj.__qualname__}` "
        "(e.g. `my_package.a_module:some_function`)",
    )
    menus: Optional[List[MenuRule]] = Field(
        None,
        description="(Optional) Menus to which this action should be added.",
    )
    keybindings: Optional[List[KeyBindingRule]] = Field(
        None,
        description="(Optional) Default keybinding(s) that will trigger this command.",
    )
    add_to_command_palette: bool = Field(
        True,
        description="Whether to add this command to the global Command Palette "
        "during registration.",
    )

    @validator("callback")
    def _validate_callback(callback: object) -> Union[Callable, str]:
        """Assert that `callback` is a callable or valid fully qualified name."""
        if callable(callback):
            return callback
        elif isinstance(callback, str):
            return _validate_python_name(str(callback))
        raise TypeError("callback must be a callable or a string")  # pragma: no cover

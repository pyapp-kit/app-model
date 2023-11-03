from typing import TYPE_CHECKING, Callable, Generic, List, Optional, TypeVar, Union

from pydantic_compat import Field, field_validator

from ._command_rule import CommandRule
from ._keybinding_rule import KeyBindingRule
from ._menu_rule import MenuRule
from ._utils import _validate_python_name

# maintain runtime compatibility with older typing_extensions
if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")
else:
    try:
        from typing_extensions import ParamSpec

        P = ParamSpec("P")
    except ImportError:
        P = TypeVar("P")
R = TypeVar("R")


class Action(CommandRule, Generic[P, R]):
    """An Action is a callable object with menu placement, keybindings, and metadata.

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
        description="(Optional) Menus to which this action should be added.  Note that "
        "menu items in the sequence may be supplied as a plain string, which will "
        "be converted to a `MenuRule` with the string as the `id` field.",
    )
    keybindings: Optional[List[KeyBindingRule]] = Field(
        None,
        description="(Optional) Default keybinding(s) that will trigger this command.",
    )
    palette: bool = Field(
        True,
        description="Whether to add this command to the global Command Palette "
        "during registration.",
    )

    @field_validator("callback")
    def _validate_callback(callback: object) -> Union[Callable, str]:
        """Assert that `callback` is a callable or valid fully qualified name."""
        if callable(callback):
            return callback
        elif isinstance(callback, str):
            return _validate_python_name(str(callback))
        raise TypeError("callback must be a callable or a string")  # pragma: no cover

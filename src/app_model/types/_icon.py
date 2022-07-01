from typing import Any, Callable, Generator, NewType, Optional, TypedDict, Union

from pydantic import Field

from ._base import _StrictModel

IconCodeStr = NewType("IconCodeStr", str)


class Icon(_StrictModel):
    """Icons used to represent commands, or submenus.

    May provide both a light and dark variant.  If only one is provided, it is used
    in all theme types.
    """

    dark: Optional[IconCodeStr] = Field(
        None,
        description="Icon path when a dark theme is used. These may be superqt "
        "fonticon keys, such as `fa5s.arrow_down`",
    )
    light: Optional[IconCodeStr] = Field(
        None,
        description="Icon path when a light theme is used. These may be superqt "
        "fonticon keys, such as `fa5s.arrow_down`",
    )

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> "Icon":
        """Validate icon."""
        # if a single string is passed, use it for both light and dark.
        if isinstance(v, str):
            v = {"dark": v, "light": v}
        return cls(**v)


class IconDict(TypedDict):
    """Icon dictionary."""

    dark: Optional[IconCodeStr]
    light: Optional[IconCodeStr]


IconOrDict = Union[Icon, IconDict]
